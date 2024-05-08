from enum import Enum


class EnumObjectType(str, Enum):
    NotSet = 'NotSet'
    Alien = 'Alien'
    Player = 'Player'
    Rocket = 'Rocket'
    Wall = 'Wall'
    
    def __str__(self) -> str:
        return self.value
    