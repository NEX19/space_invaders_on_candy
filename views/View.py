from controllers.GameController import GameController

from models.GameData import GameData
from models.Explosion import Explosion
from models.GameObject import GameObject
from models.constants import *
from models.enums.EnumPlayerTurns import EnumPlayerTurns
from models.enums.EnumObjectType import EnumObjectType

from views.menus.MainMenu import MainMenu
from views.menus.LoadMenu import LoadMenu

from time import sleep
import pygame
from pygame.locals import *
import os
from typing import List
import numpy as np


class View:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.__controller: GameController = GameController.instance()
        self.__fps: int = 60
        self.__win = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.__fullscreen_display = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Space invaders")
        self.__save_cooldown: int = 0
        self.font = pygame.font.Font("resources/fonts/RetroGaming.ttf", 36)
        # images
        self.images = {}
        self.images["invader1_1"] = pygame.image.load("resources/sprites/invader1_1.png")
        self.images["invader1_1"] = pygame.transform.scale(self.images["invader1_1"], (35, 25))
        self.images["invader1_2"] = pygame.image.load("resources/sprites/invader1_2.png")
        self.images["invader1_2"] = pygame.transform.scale(self.images["invader1_2"], (35, 25))
        self.images["invader2_1"] = pygame.image.load("resources/sprites/invader2_1.png")
        self.images["invader2_1"] = pygame.transform.scale(self.images["invader2_1"], (35, 25))
        self.images["invader2_2"] = pygame.image.load("resources/sprites/invader2_2.png")
        self.images["invader2_2"] = pygame.transform.scale(self.images["invader2_2"], (35, 25))
        self.images["invader3_1"] = pygame.image.load("resources/sprites/invader3_1.png")
        self.images["invader3_1"] = pygame.transform.scale(self.images["invader3_1"], (35, 25))
        self.images["invader3_2"] = pygame.image.load("resources/sprites/invader3_2.png")
        self.images["invader3_2"] = pygame.transform.scale(self.images["invader3_2"], (35, 25))

        self.player_image = pygame.image.load("resources/sprites/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))

        self.explosion_image = pygame.image.load("resources/sprites/explosion.png")
        self.explosion_image = pygame.transform.scale(self.explosion_image, (35, 25))

        self.current_degree = 0
        self.current_wave = 0
        self.recoil_mult = 1
        self.rotation_degree = 90

    def main(self):
        running = True
        main_menu = MainMenu(self.__win, self.__fullscreen_display)
        while running:
            game_was_chosen: bool = False
            option: str = main_menu.run()
            if option == "QUIT":
                pygame.quit()
                running = False
            elif option == "NEW GAME":
                self.__controller.load_game("starting_position.bin")
                game_was_chosen = True
            elif option == "LOAD GAME":
                load_menu = LoadMenu(self.__win, self.__fullscreen_display)
                chosen_game: str = load_menu.run()
                self.__controller.load_game(chosen_game)
                game_was_chosen = True
            
            if game_was_chosen:
                    self.game_loop()


    def handle_input(self) -> List[EnumPlayerTurns]:
        keys: List[EnumPlayerTurns] = [EnumPlayerTurns.NotSet]
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_LEFT]:
            keys.append(EnumPlayerTurns.Left)
        if key_input[pygame.K_RIGHT]:
            keys.append(EnumPlayerTurns.Right)
        if key_input[pygame.K_SPACE]:
            keys.append(EnumPlayerTurns.Fire)
        if key_input[pygame.K_s]:
            keys.append(EnumPlayerTurns.Save)
        if key_input[pygame.K_ESCAPE]:
            keys.append(EnumPlayerTurns.Exit)
        return keys

    def print_to_center(self, message: str) -> None:
        self.__win.fill((0, 0, 0))
        text = self.font.render(message, True, (255, 255 ,255))
        rect = text.get_rect()
        rect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.__win.blit(text, rect)
        pygame.transform.scale(self.__win, (1920, 1080), self.__fullscreen_display)
        pygame.display.update()
        sleep(1)

    def game_loop(self) -> None:
        clock = pygame.time.Clock()
        game_is_running = True
        last_action_time = pygame.time.get_ticks()
        last_color_switch = pygame.time.get_ticks()
        interval = 1000
        color_interval = 250
        while game_is_running:
            clock.tick(self.__fps)
            turn: List[EnumPlayerTurns] = self.handle_input() 

            if EnumPlayerTurns.Exit in turn:
                break

            if EnumPlayerTurns.Fire in turn:
                # if self.current_wave > 0:
                    self.current_degree += 1
            else:
                self.current_degree = 0

            current_time = pygame.time.get_ticks()
            if current_time - last_action_time >= interval:
                last_action_time = current_time
                if self.rotation_degree != 0:
                    self.rotation_degree += 90
            
            if current_time - last_color_switch >= color_interval:

                last_color_switch = current_time
                

            if EnumPlayerTurns.Save in turn and self.__save_cooldown == 0:
                self.__save_cooldown = 5 * self.__fps
                self.__controller.save_game()

            game_status = self.__controller.update_game(turn)
            data = self.__controller.get_data() 
            self.render_objects(data)
            pygame.event.pump()
            self.__save_cooldown = max(0, self.__save_cooldown - 1)
            
            if game_status == 1:
                self.print_to_center("YOU SECURED THIS ROUND")
                self.print_to_center("PREPARE FOR NEXT ONE...")

                if self.current_wave == 0:
                    self.recoil_mult = 2
                    self.rotation_degree = 90
                elif self.current_wave == 1:
                    self.rotation_degree = 90

                self.current_wave += 1
                self.__controller.load_next_round(speed_surplus=self.current_wave)
            elif game_status == -1:
                self.print_to_center(f'YOU GOT {data.score} POINTS')
                break
        

    def render_objects(self, data: GameData) -> None:
        self.__win.fill((0, 0, 0))
        for obj in data.objects:
            if obj.object_type is EnumObjectType.Rocket:
                pygame.draw.rect(self.__win, (255, 255, 255), obj.get_cords())
            elif obj.object_type is EnumObjectType.Wall:
                pygame.draw.rect(self.__win, (0, 255, 0), obj.get_cords())
        for obj in data.objects:
            if obj.object_type is EnumObjectType.Alien:
                self.__win.blit(self.images[f'{obj.name}_{data.current_alien_frame + 1}'], (obj.position.x, obj.position.y))
        self.__win.blit(self.player_image, (data.player.position.x, data.player.position.y))

        for expl in data.explosions:
            self.__win.blit(self.explosion_image, (expl.position.x, expl.position.y))
        
        
        # player stats
        pygame.draw.rect(self.__win, (0, 0, 0), (0, 0, 1000, 80))
        pygame.draw.rect(self.__win, (255, 255, 255), (0, 0, 1000, 80), 2)

        health_text = self.font.render(f'{data.health * "<3 "}', True, (255, 0, 0))  
        health_rect = health_text.get_rect()
        health_rect.center = (120, 40) 
        self.__win.blit(health_text, health_rect)
        higscore_text = self.font.render(f'SCORE: {data.score}', True, (255, 255 ,255))
        higscore_rect = higscore_text.get_rect()
        higscore_rect.center = (800, 40)
        self.__win.blit(higscore_text, higscore_rect)

        # self.__win = pygame.transform.rotate(self.__win, 0.1)

        # self.current_degree += 0.5

        # game_over_screen_fade = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        # game_over_screen_fade.fill((255, 255, 255))
        # game_over_screen_fade.set_alpha(160)

        # self.__win.blit(game_over_screen_fade, (0, 0))

        pixels = pygame.surfarray.pixels2d(self.__win)
        # pixels ^= 0 if ((pygame.time.get_ticks() // 1000) % 2) else 2 ** 32 - 2 ** 10
        pixels ^= 2 ** 32 - 2 ** (pygame.time.get_ticks() // 100 % 31)
        del pixels

        self.__win.blit(pygame.transform.rotate(self.__win, np.sin(self.current_degree) * self.recoil_mult + self.rotation_degree), (0, 0))
        pygame.transform.scale(self.__win, (1920, 1080), self.__fullscreen_display)
        pygame.display.update()