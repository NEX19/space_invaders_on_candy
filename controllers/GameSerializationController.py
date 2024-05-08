from models.GameData import GameData
from models.constants import ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_SPEED, WALL_HEIGHT, WALL_WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_SPEED, ROCKET_WIDTH, ROCKET_HEIGHT, ROCKET_SPEED
from models.GameObject import GameObject
from models.enums.EnumObjectType import EnumObjectType
from models.Vector2D import Vector2D
#from models.constants import 

import struct
import sys

GAMEOBJECT_BYTE_COUNT = 20
EXPLOSION_BYTE_COUNT = 12
INT_BYTE_COUNT = 4

class GameSerializationController:
    __instance = None

    @staticmethod
    def instance():
        if GameSerializationController.__instance is None:
            GameSerializationController.__instance = GameSerializationController()
        return GameSerializationController.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance is allowed")
        self.__instance = self

    def gameobject_of_type_count(self, game_data: GameData, object_type: EnumObjectType) -> int:
        count: int = 0
        for obj in game_data.objects:
            if obj.object_type == object_type:
                count += 1
        return count

    def create_new_game(self) -> GameData:
        starting_position = GameData()
        for i in range(2):
            for j in range(10): 
                starting_position.objects.append(
                    GameObject(
                        EnumObjectType.Alien,
                        Vector2D(j * 70 + 10, i * 70 + 100),
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                        "invader1",
                        ALIEN_SPEED,
                        Vector2D(1, 0)
                        ))
        for i in range(2):
            for j in range(10):
                starting_position.objects.append(
                    GameObject(
                        EnumObjectType.Alien,
                        Vector2D(j * 70 + 10, i * 70 + 240),
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                        "invader2",
                        ALIEN_SPEED,
                        Vector2D(1, 0)
                        ))
        for i in range(2):
            for j in range(10):
                starting_position.objects.append(
                    GameObject(
                        EnumObjectType.Alien,
                        Vector2D(j * 70 + 10, i * 70 + 380),
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                        "invader3",
                        ALIEN_SPEED,
                        Vector2D(1, 0)
                        ))
        for i in range(2):
            for j in range(4):
                for k in range(5):
                    starting_position.objects.append(
                    GameObject(
                        EnumObjectType.Wall,
                        Vector2D(225 * j + 100 + k * 25, 800 + i * 25),
                        WALL_WIDTH,
                        WALL_HEIGHT,
                        "wall",
                        0,
                        Vector2D(0, 0)
                        ))
        for j in range(4):
            for k in range(2):
                starting_position.objects.append(
                    GameObject(
                        EnumObjectType.Wall,
                        Vector2D(225 * j + 100 + k * 100, 850),
                        WALL_WIDTH,
                        WALL_HEIGHT,
                        "wall",
                        0,
                        Vector2D(0, 0)
                        ))

        ALIEN_SPEED += 1
        print(ALIEN_SPEED)
        return starting_position

    def pack_gameobject(self, obj: GameObject) -> bytes:
        data = struct.pack('5i',
                        obj.position.x,
                        obj.position.y,
                        obj.direction.x,
                        obj.direction.y,
                        ord(obj.name[-1]) - ord('0'))
        return data

    def transfer_data_to_bin(self, file_name: str, game_data: GameData):
        with open(f'saves/{file_name}', 'wb') as file:
            id = struct.pack('i', 1) # aliens
            length = struct.pack('i', self.gameobject_of_type_count(game_data, EnumObjectType.Alien))
            file.write(id) 
            file.write(length)
            i: int = 0
            for obj in game_data.objects:
                if obj.object_type != EnumObjectType.Alien:
                    continue
                sub_id = struct.pack('i', i)
                data = self.pack_gameobject(obj)
                file.write(sub_id)
                file.write(data)

            id = struct.pack('i', 2) # walls
            length = struct.pack('i', self.gameobject_of_type_count(game_data, EnumObjectType.Wall))
            file.write(id) 
            file.write(length)
            i: int = 0
            for obj in game_data.objects:
                if obj.object_type != EnumObjectType.Wall:
                    continue
                sub_id = struct.pack('i', i)
                data = self.pack_gameobject(obj)
                file.write(sub_id)
                file.write(data)

            id = struct.pack('i', 3) # rockets
            length = struct.pack('i', self.gameobject_of_type_count(game_data, EnumObjectType.Rocket))
            file.write(id) 
            file.write(length)  
            i: int = 0
            for obj in game_data.objects:
                if obj.object_type != EnumObjectType.Rocket:
                    continue
                sub_id = struct.pack('i', i)
                data = self.pack_gameobject(obj)
                file.write(sub_id)
                file.write(data)

            id = struct.pack('i', 4) # player
            player = self.pack_gameobject(game_data.player)
            file.write(id)
            file.write(player)

            id = struct.pack('i', 5) # game_variables  
            game_variables = struct.pack('7i', game_data.score, game_data.health, game_data.player_shot_cooldown,
                                game_data.alien_shot_cooldown, game_data.alien_leap_countdown, game_data.alien_animation_countdown,
                                game_data.current_alien_frame)
            file.write(id)
            file.write(game_variables)
            
    def read_data_from_bin(self, file_name: str) -> GameData:
        game_data = GameData()
        with open(f'saves/{file_name}', 'rb') as file:
            id_bin = file.read(INT_BYTE_COUNT) # id - 1, aliens list
            length_bin = file.read(INT_BYTE_COUNT)
            length, = struct.unpack('i', length_bin)
            for i in range(length):
                sub_id = file.read(4)
                alien_data = file.read(GAMEOBJECT_BYTE_COUNT)
                pos_x, pos_y, dir_x, dir_y, num = struct.unpack('5i', alien_data)
                alien = GameObject(EnumObjectType.Alien, 
                            Vector2D(pos_x, pos_y),
                            ALIEN_WIDTH,
                            ALIEN_HEIGHT,
                            f'invader{num}',
                            ALIEN_SPEED,
                            Vector2D(dir_x, dir_y))
                game_data.objects.append(alien)

            id_bin = file.read(INT_BYTE_COUNT) # id - 2, walls list
            length_bin = file.read(INT_BYTE_COUNT)
            length, = struct.unpack('i', length_bin)
            for i in range(length):
                sub_id = file.read(4)
                wall_data = file.read(GAMEOBJECT_BYTE_COUNT)
                pos_x, pos_y, dir_x, dir_y, num = struct.unpack('5i', wall_data)
                wall = GameObject(EnumObjectType.Wall, 
                            Vector2D(pos_x, pos_y),
                            WALL_WIDTH,
                            WALL_HEIGHT,
                            f'wall',
                            0,
                            Vector2D(dir_x, dir_y))
                game_data.objects.append(wall)

            id_bin = file.read(INT_BYTE_COUNT) # id - 3, rocket list
            length_bin = file.read(INT_BYTE_COUNT)
            length, = struct.unpack('i', length_bin)
            for i in range(length):
                sub_id = file.read(4)
                rocket_data = file.read(GAMEOBJECT_BYTE_COUNT)
                pos_x, pos_y, dir_x, dir_y, num = struct.unpack('5i', rocket_data)
                speed_mult: int = 1
                if dir_y == -1:
                    speed_mult = 2
                rocket = GameObject(EnumObjectType.Rocket, 
                            Vector2D(pos_x, pos_y),
                            ROCKET_WIDTH,
                            ROCKET_HEIGHT,
                            f'rocket',
                            ROCKET_SPEED * speed_mult,
                            Vector2D(dir_x, dir_y))
                game_data.objects.append(rocket)
            
            id = file.read(INT_BYTE_COUNT) # id - 2, player
            player_data = file.read(GAMEOBJECT_BYTE_COUNT)
            pos_x, pos_y, dir_x, dir_y, num = struct.unpack('5i', player_data)
            player = GameObject(EnumObjectType.Player,
                                Vector2D(pos_x, pos_y), 
                                PLAYER_WIDTH,
                                PLAYER_HEIGHT,
                                "player",
                                PLAYER_SPEED,
                                Vector2D(dir_x, dir_y))
            game_data.player = player

            id = file.read(INT_BYTE_COUNT) # id - 3, game variables
            game_variables = file.read(7 * INT_BYTE_COUNT)
            game_data.score, game_data.health, game_data.player_shot_cooldown, game_data.alien_shot_cooldown, game_data.alien_leap_countdown, game_data.alien_animation_countdown, game_data.current_alien_frame = struct.unpack('7i', game_variables)
        return game_data
