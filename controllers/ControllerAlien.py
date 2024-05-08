from models.GameObject import GameObject
from models.enums.EnumObjectType import EnumObjectType
from models.GameData import GameData
from models.constants import MAP_WIDTH, ALIEN_HEIGHT, ALIEN_WIDTH, LAST_RESORT_LINE

from controllers.interfaces.IControllerObject import IControllerObject


class ControllerAlien(IControllerObject):
    def __init__(self, alien: GameObject, func_on_bottom_reach: callable, speed_surplus: int = 0):
        if alien.object_type is not EnumObjectType.Alien:
            raise Exception("ControllerAlien can only use EnumObjectType.Alien type objects")
        self.__alien: GameObject = alien
        self.__listeners_border_reach: List[callable] = []
        self.__direction_update_needed: bool = False
        self.__bottom_reach_listener: callable = func_on_bottom_reach
        self.speed_surplus = speed_surplus

    def move(self):
        self.__alien.position.x = max(0, min(MAP_WIDTH - self.__alien.width, self.__alien.position.x + self.__alien.direction.x * (self.__alien.speed + self.speed_surplus)))
        if self.__alien.position.x == 0 or self.__alien.position.x == MAP_WIDTH - self.__alien.width:
            self.notify_listeners()
            self.__direction_update_needed = True
        if self.__alien.position.y >= LAST_RESORT_LINE:
            self.__bottom_reach_listener()

    @property
    def obj(self):
        return self.__alien

    def update(self):
        if self.__direction_update_needed:
            self.__direction_update_needed = False
            self.__alien.direction = -self.__alien.direction
            self.__alien.position.y += ALIEN_HEIGHT

    def on_border_reach(self):
        self.__direction_update_needed = True

    def notify_listeners(self):
        for listener in self.__listeners_border_reach:
            listener()

    def add_listener_border_reach(self, func_on_border_reach):
        if func_on_border_reach not in self.__listeners_border_reach:
            self.__listeners_border_reach.append(func_on_border_reach)

    def remove_listener_border_reach(self, func_on_border_reach):
        if func_on_border_reach in self.__listeners_border_reach:
            self.__listeners_border_reach.remove(func_on_border_reach)