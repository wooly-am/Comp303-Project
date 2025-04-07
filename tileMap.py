from .imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import Player

SOUND_FILEPATHS = [
    "sound/fest/i1.wav", "sound/fest/i2.wav", "sound/fest/i3.wav", "sound/fest/i4.wav",
    "sound/fest/arp1.wav",
    "sound/fest/yeah.wav",
    "sound/fest/awful.wav",
    "sound/fest/clarinet.wav",
    "sound/fest/replacement.wav",
    "sound/fest/bass.wav",
    "sound/fest/guitar1.wav",
    "sound/fest/guitar2.wav",
    "sound/fest/drum1.wav",
    "sound/fest/drums2.wav",
    "sound/fest/drums3.wav",
    "sound/fest/drums4s.wav",
    "sound/fest/backing_track.wav"
]

class FlyweightTile:
    """ Flyweight class representing an abstract tile defined by coordinate boundaries. """
    _instances = {}  # Dictionary to store shared FlyweightTile instances


    def __new__(cls, tile_id: int, top_left: tuple[int, int], bottom_right: tuple[int, int],sound_path: str=None,is_number_sequence_tile: bool = False):
        """ Create or return an existing FlyweightTile instance. """
        # Use the tile_id and coordinates as the key
        key = (tile_id, top_left, bottom_right)

        # Check if the FlyweightTile already exists
        if key not in cls._instances:
            # Create a new FlyweightTile instance
            instance = super().__new__(cls)
            instance.tile_id = tile_id
            instance.top_left = top_left
            instance.bottom_right = bottom_right
            instance.sound_path = sound_path
            instance.is_number_sequence_tile = is_number_sequence_tile
            instance.stored_sequence = [4,4,8,8] if is_number_sequence_tile else None
            cls._instances[key] = instance  # Store the instance
        else:
            # Return the existing instance
            instance = cls._instances[key]

        return instance


    def get_sound_filepath(self) -> str | None:
        """ Return the sound filepath for this tile. """
        return self.sound_path

    def get_tile_id(self) -> int:
        """ Return the tile ID. """
        return self.tile_id


    def store_number(self, number: int):
        """ Store a number in the tile's sequence if it's a number-sequence tile. """
        if self.is_number_sequence_tile:
            self.stored_sequence.append(number)  # Store the number for later use


    def get_stored_sequence(self):
        """ Get the stored sequence (only for number-sequence tiles). """
        return self.stored_sequence if self.is_number_sequence_tile else None

    def clear_stored_sequence(self):
        pass


class TileMap:
    """ A Flyweight tile system where tiles exist only as coordinate ranges. """
    def __init__(self, start_y: int, start_x: int, tile_size: int = 4):
        self.tiles: dict[tuple[tuple[int, int], tuple[int, int]], FlyweightTile] = {}  # Store FlyweightTile instances
        self.tile_size = tile_size
        self.generate_tiles(start_y, start_x)
        self.current_tile_for_player: dict[str, FlyweightTile | None] = {}
        self.observers = []
    def add_observer(self, callback):
        self.observers.append(callback)



    def generate_tiles(self, start_y: int, start_x: int):
        """ Generates a 4x4 grid of abstract tiles and assigns a unique ID (1-16) to each tile. """
        tile_id = 1  # Unique ID for each 4x4 tile

        for row in range(4):
            for col in range(4):
                top_left = (start_y + row * self.tile_size, start_x + col * self.tile_size)
                bottom_right = (top_left[0] + self.tile_size - 1, top_left[1] + self.tile_size - 1)
                sound_path = SOUND_FILEPATHS[tile_id - 1]

                # Create or retrieve a FlyweightTile instance using the Flyweight pattern
                is_number_sequence_tile = tile_id in {1, 2, 3, 4}
                flyweight_tile = FlyweightTile(tile_id, top_left, bottom_right,sound_path,is_number_sequence_tile)
                self.tiles[(top_left, bottom_right)] = flyweight_tile  # Store the FlyweightTile instance

                tile_id += 1


    def check_player_position(self, player: Player) -> tuple[int | None, FlyweightTile | None, str | None]:
        player_position = player.get_current_position()
        player_pos_tuple = (player_position.y, player_position.x)


        matched_tile = None
        for (top_left, bottom_right), flyweight_tile in self.tiles.items():
            if (top_left[0] <= player_pos_tuple[0] <= bottom_right[0] and
                    top_left[1] <= player_pos_tuple[1] <= bottom_right[1]):
                matched_tile = flyweight_tile
                break


        old_tile = self.current_tile_for_player.get(player.get_name(), None)


        if old_tile is not None and old_tile != matched_tile:
            if old_tile.is_number_sequence_tile:
                old_tile.stored_sequence = []


            if len(self.observers) > 0:
                funfest_house = self.observers[0]
                self.observers[0].notify_tile_deactivation(old_tile, player)
                funfest_house.remove_tile_loop(old_tile, player)
        # Did the player just move onto a new tile?
        if matched_tile is not None and matched_tile != old_tile:
            if len(self.observers) > 0:
                funfest_house = self.observers[0]
                self.observers[0].notify_tile_activation(matched_tile, player)
                funfest_house.on_tile_activated(matched_tile)
        # Update the player’s current tile reference
        self.current_tile_for_player[player.get_name()] = matched_tile
        if matched_tile:
            return matched_tile.tile_id, matched_tile, matched_tile.sound_path
        else:
            return None, None, None

class Observer:
    def __init__(self,player):
        self.player_id= player.get_name()
        self.observers = []
        self.player=player
        self.sequence = [[],[],[],[]]

    def notify_tile_activation(self, tile, player):
        for observer in self.observers:
            observer.on_tile_activated(tile, player)


    def notify_tile_deactivation(self, tile, player):
        for observer in self.observers:
            observer.on_tile_deactivated(tile, player)

    def notify_sequence_update(self, tile):
        for observer in self.observers:
            observer.on_sequence_update(tile)


    def add_observer(self, callback):
        self.observers.append(callback)

