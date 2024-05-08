from abc import ABC, abstractmethod

class IControllerObject(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def obj(self):
        pass
    
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def update(self):
        pass
