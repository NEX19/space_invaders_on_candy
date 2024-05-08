from models.GameObject import GameObject
from models.constants import MAP_HEIGHT, MAP_WIDTH, ALIEN_HEIGHT, PLAYER_SHOT_COOLDOWN, ROCKET_SPEED
from models.enums.EnumObjectType import EnumObjectType
from models.enums.EnumPlayerTurns import EnumPlayerTurns
from models.Vector2D import Vector2D
from models.GameData import GameData

from controllers.interfaces.IControllerObject import IControllerObject

from typing import List

class ControllerPlayer(IControllerObject):
    def __init__(self, player: GameObject, func_on_fire: callable, game_state: GameData):
        if player.object_type is not EnumObjectType.Player:
            raise Exception("ControllerPlayer can only use EnumObjectType.Player type objects")
        self.__player: GameObject = player
        self.__fire_listener: callable = func_on_fire
        self.__game_state: GameData = game_state

    def move(self):
        self.__player.position.x = max(0, min(MAP_WIDTH - self.__player.width, self.__player.position.x + self.__player.direction.x * self.__player.speed)) 

    def update(self, turn: List[EnumPlayerTurns]):
        direction: int = 0 
        if EnumPlayerTurns.Left in turn:
            direction -= 1
        if EnumPlayerTurns.Right in turn:
            direction += 1
        self.__player.direction.x = direction
        if EnumPlayerTurns.Fire in turn and self.__game_state.player_shot_cooldown == 0:
            self.__game_state.player_shot_cooldown = PLAYER_SHOT_COOLDOWN 
            x: int = self.__player.position.x + 20
            y: int = self.__player.position.y - 20
            self.__fire_listener(x, y, "rocket", Vector2D(0, -1), ROCKET_SPEED * 2)

    @property
    def obj(self):
            return self.__player

