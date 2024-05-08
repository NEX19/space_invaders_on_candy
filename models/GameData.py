from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from models.Vector2D import Vector2D
from models.GameObject import GameObject
from models.Explosion import Explosion
from models.constants import ALIEN_ANIMATION_COUNTDOWN, PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_SPEED
from models.enums.EnumObjectType import EnumObjectType

@dataclass_json
@dataclass
class GameData:
    objects: List[GameObject] = field(default_factory=list)
    player: GameObject = field(default_factory=lambda: 
                            GameObject(
                            EnumObjectType.Player,
                            Vector2D(450, 930),
                            PLAYER_WIDTH,
                            PLAYER_HEIGHT,
                            "player",
                            PLAYER_SPEED,
                            Vector2D(0, 0)))
    score: int = 0
    health: int = 3
    player_shot_cooldown: int = 0
    alien_shot_cooldown: int = 0
    alien_leap_countdown: int = 0 
    explosions: List[Explosion] = field(default_factory=list)
    alien_animation_countdown: int = ALIEN_ANIMATION_COUNTDOWN # when becomes zero, aliens should change sprite
    current_alien_frame: int = 0

