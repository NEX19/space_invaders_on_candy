import pygame
from pygame.locals import *
import os
from typing import List

from views.menus.Menu import Menu

class LoadMenu(Menu):
    def __init__(self, window: pygame.surface.Surface, fullscreen):
        options: List[str] = []
        if not os.listdir("saves"):
            options.append("THERE'S NOTHING TO LOAD")
        else:
            options = os.listdir("saves")
        options.sort()
        super().__init__(options, window, fullscreen)

    def draw_menu(self):
        start_index = self.selected_option // 25 * 25
        end_index = min(len(self.options), start_index + 25)
        for i, option in enumerate(self.options[start_index : end_index]):
            if start_index + i == self.selected_option:
                text = self.font.render(option, True, (0, 255, 0))  
            else:
                text = self.font.render(option, True, (255, 255, 255))  
            rect = text.get_rect()
            rect.center = (self.win.get_width() // 2, 20 + i * 40)
            self.win.blit(text, rect)
        pygame.transform.scale(self.win, (1920, 1080), self.fullscreen)

