from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from models.Vector2D import Vector2D
from models.constants import ALIEN_HEIGHT, ALIEN_WIDTH


@dataclass_json
@dataclass
class Explosion:
    position: Vector2D
    width: int = ALIEN_WIDTH
    height: int = ALIEN_HEIGHT
    name: str = "explosion"
    explosion_countdown: int = 5 # when it becomes zero, it ceases to exist