from enum import Enum


class EnumPlayerTurns(str, Enum):
    NotSet = 'NotSet'
    Left = 'Left'
    Right = 'Right'
    Fire = 'Fire'
    Save = 'Save'
    Exit = 'Exit'
    
    def __str__(self) -> str:
        return self.value
    