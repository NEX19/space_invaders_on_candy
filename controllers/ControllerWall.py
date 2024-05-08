from controllers.interfaces.IControllerObject import IControllerObject

from models.GameObject import GameObject
from models.enums.EnumObjectType import EnumObjectType

class ControllerWall(IControllerObject):
    def __init__(self, wall: GameObject):
        if wall.object_type is not EnumObjectType.Wall:
            raise Exception("ControllerWall can only use EnumObjectType.Wall type objects")
        self.__wall: GameObject = wall
    
    def move(self):
        pass

    def update(self):
        pass

    @property
    def obj(self):
        return self.__wall

