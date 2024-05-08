from models.GameData import GameData
from models.constants import MAP_HEIGHT, MAP_WIDTH, ALIEN_ANIMATION_COUNTDOWN, ALIEN_HEIGHT, ALIEN_WIDTH, ROCKET_HEIGHT, ROCKET_WIDTH, ALIEN_SPEED, ROCKET_SPEED
from models.Vector2D import Vector2D
from models.GameObject import GameObject
from models.enums.EnumPlayerTurns import EnumPlayerTurns
from models.enums.EnumObjectType import EnumObjectType
from models.Explosion import Explosion

from controllers.ControllerAlien import ControllerAlien
from controllers.ControllerPlayer import ControllerPlayer
from controllers.ControllerRocket import ControllerRocket
from controllers.ControllerWall import ControllerWall
from controllers.interfaces.IControllerObject import IControllerObject
from controllers.enums.EnumAlienEventType import EnumAlienEventType
from controllers.interfaces.IControllerObject import IControllerObject
from controllers.GameSerializationController import GameSerializationController

import random
import pickle
import pygame
import json
import time
import os

from typing import List
from datetime import datetime


class GameController:
    __instance = None

    #
    # interface for view module
    #

    @staticmethod
    def instance():
        if GameController.__instance is None:
            GameController.__instance = GameController()
        return GameController.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance is allowed")
        self.__instance = self
        self.__data = GameData()
        self.__aliens_reached_bottom: bool = False
        self.__controllers: List[IControllerObject] = []
        self.__player_controller: ControllerPlayer = None
        self.__serialization_controller = GameSerializationController.instance()

    def load_game(self, file_name: str, speed_surplus: int = 0):
        self.__data = self.__serialization_controller.read_data_from_bin(file_name)
        self.__create_controllers_for_model(speed_surplus)
        self.__tie_aliens()
        
    def save_game(self):
        file_name: str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.bin")
        self.__serialization_controller.transfer_data_to_bin(file_name, self.__data)

    def load_next_round(self, speed_surplus: int = 0):
        score = self.__data.score
        self.load_game("starting_position.bin", speed_surplus)
        self.__data.score = score

    # -1 - lose, 0 - continues, 1 - round secured
    def update_game(self, turn: List[EnumPlayerTurns]) -> int:
        for controller in self.__controllers:
            controller.move()
        self.__player_controller.move()

        for controller in self.__controllers:
            controller.update()
        self.__player_controller.update(turn)

        if self.__data.alien_shot_cooldown == 0:
            self.__invoke_alien_attack()

        self.__data.player_shot_cooldown = max(0, self.__data.player_shot_cooldown - 1)
        self.__data.alien_shot_cooldown = max(0, self.__data.alien_shot_cooldown - 1)
        self.__data.alien_leap_countdown = max(0, self.__data.alien_leap_countdown - 1)


        if self.__data.alien_animation_countdown == 0:
            self.__data.alien_animation_countdown = ALIEN_ANIMATION_COUNTDOWN
            self.__data.current_alien_frame = 1 - self.__data.current_alien_frame
        self.__data.alien_animation_countdown = max(0, self.__data.alien_animation_countdown - 1)

        for expl in self.__data.explosions:
            expl.explosion_countdown = max(0, expl.explosion_countdown - 1)
            if expl.explosion_countdown == 0:
                self.__data.explosions.remove(expl)

        game_status: int = 0

        has_aliens = any(isinstance(con, ControllerAlien) for con in self.__controllers)

        if not has_aliens:
            game_status = 1

        if self.__data.health <= 0 or self.__aliens_reached_bottom:
            game_status = -1

        self.__aliens_reached_bottom = False

        return game_status

    def get_data(self):
        return self.__data

    # 
    # in-game logic
    #  

    def __create_controllers_for_model(self, speed_surplus: int = 0):
        self.__controllers = []
        self.__player_controller = None

        self.__player_controller = ControllerPlayer(self.__data.player, self.__launch_rocket, self.__data)

        for obj in self.__data.objects:
            if obj.object_type is EnumObjectType.Alien:
                self.__controllers.append(ControllerAlien(obj, self.__on_bottom_reach, speed_surplus))
            elif obj.object_type is EnumObjectType.Wall:
                self.__controllers.append(ControllerWall(obj))
            elif obj.object_type is EnumObjectType.Rocket:
                self.__controllers.append(ControllerRocket(obj, self.__on_rocket_collision, self.__controllers, self.__player_controller))
        

    def __on_bottom_reach(self):
        self.__aliens_reached_bottom = True

    def __tie_aliens(self):
        for i in self.__controllers:
            if i.obj.object_type is not EnumObjectType.Alien:
                continue
            for alien in self.__controllers:
                if alien.obj.object_type is not EnumObjectType.Alien or i is alien:
                    continue
                i.add_listener_border_reach(alien.on_border_reach)

    def __on_rocket_collision(self, target: IControllerObject):
        if target.obj.object_type is EnumObjectType.Player:
            self.__data.health -= 1
        elif target.obj.object_type is EnumObjectType.Alien: 
            self.__data.score += 50
            self.__data.explosions.append(Explosion(position=target.obj.position))
            for alien in self.__controllers:
                if alien.obj.object_type is not EnumObjectType.Alien:
                    continue
                alien.remove_listener_border_reach(target.on_border_reach)
            self.__data.objects.remove(target.obj)
            self.__controllers.remove(target)
        else:
            self.__data.objects.remove(target.obj)
            self.__controllers.remove(target) 
        
    def __launch_rocket(self, x, y, name, direction: Vector2D, speed):
        rocket = GameObject(
            EnumObjectType.Rocket,
            Vector2D(x,y),
            ROCKET_WIDTH,
            ROCKET_HEIGHT,
            name,
            speed,
            direction)
        self.__data.objects.append(rocket)
        self.__controllers.append(ControllerRocket(rocket, self.__on_rocket_collision, self.__controllers, self.__player_controller))

    def __invoke_alien_attack(self):
        self.__data.alien_shot_cooldown = 90

        aliens: List[GameObject] = []
        chosen: List[GameObject] = []
        
        for obj in self.__data.objects:
            if obj.object_type is EnumObjectType.Alien:
                aliens.append(obj)
                
        aliens.sort(key=lambda obj: (obj.position.x, -obj.position.y))

        x = -1
        for obj in aliens:
            if x != obj.position.x:
                x = obj.position.x
                chosen.append(obj)

        for obj in random.sample(chosen, min(3, len(chosen))):
            x = obj.position.x + 15
            y = obj.position.y + 50 
            self.__launch_rocket(x, y, "rocket", Vector2D(0, 1), ROCKET_SPEED)
