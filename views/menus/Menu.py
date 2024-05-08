import pygame
from pygame.locals import *
import os

from typing import List


class Menu:
    def __init__(self, menu_options: List[str], window: pygame.surface.Surface, fullscreen):
        self.options: List[str] = menu_options
        self.font = pygame.font.Font("resources/fonts/RetroGaming.ttf", 32)
        self.selected_option = 0
        self.win = window
        self.fps = 60
        self.fullscreen = fullscreen

    def draw_menu(self) -> None:
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                text = self.font.render(option, True, (255, 0, 0)) 
            else:
                text = self.font.render(option, True, (255, 255, 255)) 
            rect = text.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 + i * 40))
            self.win.blit(text, rect)
            pygame.transform.scale(self.win, (1920, 1080), self.fullscreen)

    def run(self) -> str:
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == K_RETURN:
                        return self.options[self.selected_option]

            self.win.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.flip()