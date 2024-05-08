from models.GameObject import GameObject
from models.constants import MAP_HEIGHT, MAP_WIDTH, ALIEN_HEIGHT
from models.enums.EnumObjectType import EnumObjectType

from controllers.interfaces.IControllerObject import IControllerObject

from typing import List

class ControllerRocket(IControllerObject):
    def __init__(self, rocket: GameObject, func_on_collision: callable, controllers: List[IControllerObject], player: IControllerObject):
        if rocket.object_type is not EnumObjectType.Rocket:
            raise Exception("ControllerRocket can only use EnumObjectType.Rocket type objects")
        self.__rocket: GameObject = rocket
        self.__controllers: List[IControllerObject] = controllers 
        self.__collision_listener: callable = func_on_collision
        self.__player_controller = player

    def move(self):
        self.__rocket.position.y = max(0, min(MAP_HEIGHT, self.__rocket.position.y + self.__rocket.direction.y * self.__rocket.speed))
        if self.__rocket.position.y == 0 or self.__rocket.position.y == MAP_HEIGHT:
            self.__collision_listener(self) 

    def update(self):
        for contr in self.__controllers:
            if self.__are_intersected(contr):
                self.__collision_listener(contr)
                self.__collision_listener(self)
                break
        if self.__are_intersected(self.__player_controller):
            self.__collision_listener(self.__player_controller)
            self.__collision_listener(self)

    def __are_intersected(self, target: IControllerObject) -> bool:
        tar_x0 = target.obj.position.x 
        tar_y0 = target.obj.position.y 
        tar_x1 = tar_x0 + target.obj.width
        tar_y1 = tar_y0 + target.obj.height

        roc_x0 = self.__rocket.position.x 
        roc_y0 = self.__rocket.position.y 
        roc_x1 = roc_x0 + self.__rocket.width
        roc_y1 = roc_y0 + self.__rocket.height

        check_horizontal: bool = (tar_x0 >= roc_x1) or (tar_x1 <= roc_x0) 
        check_vertical: bool = (tar_y0 >= roc_y1) or (tar_y1 <= roc_y0)

        are_intersected: bool = not (check_horizontal or check_vertical)

        return are_intersected and target is not self 

    @property
    def obj(self):
        return self.__rocket

            

