from enum import Enum


class EnumAlienEventType(str, Enum):
    NotSet = 'NotSet'
    SideBorderReach = 'SideBorderReach'
    BottomBorderReach = 'BottomBorderReach'
    
    def __str__(self) -> str:
        return self.value