from coord import Coord
from Player import Player
from tiles.base import MapObject
from message import Message
from message import GridMessage
from funfest.fest_message import *

SOUND_FILEPATHS = [
<<<<<<< Updated upstream
    "fest/arp1.wav", "fest/arp1.wav", "fest/arp1.wav", "fest/arp1.wav",
    "fest/arp1.wav",
    "fest/backing_track.wav",
    "fest/chorus.wav",
    "fest/clarinet.wav",
    "fest/drum1.wav",
    "fest/drums2.wav",
    "fest/drums3.wav",
    "fest/guitar1.wav",
    "fest/harp1.wav",
    "fest/idkwhatthisis1.wav",
    "fest/drum1.wav",
    "fest/synth1.wav",
=======
    "sound/fest/i1.wav", "sound/fest/i2.wav", "sound/fest/i3.wav", "sound/fest/i4.wav",
    "sound/fest/arp1.wav",
    "sound/fest/backing_track.wav",
    "sound/fest/arp1.wav",
    "sound/fest/clarinet.wav",
    "sound/fest/drum1.wav",
    "sound/fest/drums2.wav",
    "sound/fest/drums3.wav",
    "sound/fest/guitar1.wav",
    "sound/fest/harp1.wav",
    "sound/fest/idkwhatthisis1.wav",
    "sound/fest/drum1.wav",
    "sound/fest/synth1.wav",
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
            instance.stored_sequence = [] if is_number_sequence_tile else None
=======
            instance.stored_sequence = [8,8,4,4] if is_number_sequence_tile else None
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        self.observers = []
    def add_observer(self, callback):
        self.observers.append(callback)

    def notify_tile_activation(self, tile):
        print(f"Tile {tile.tile_id} activated")
        for observer in self.observers:
            observer(tile)

=======
>>>>>>> Stashed changes
    def generate_tiles(self, start_y: int, start_x: int):
        """ Generates a 4x4 grid of abstract tiles and assigns a unique ID (1-16) to each tile. """
        tile_id = 1  # Unique ID for each 4x4 tile
        sound_filepaths = [
            "", "", "", "",
            "resources/sound/fest/arp1.wav",
<<<<<<< Updated upstream
            "resources/sound/fest/yeah.wav",
            "resources/sound/fest/awful.wav",
            "resources/sound/fest/clarinet.wav",
            "resources/sound/fest/replacement.wav",
=======
            "resources/sound/fest/backing_track.wav",
            "resources/sound/fest/chorus.wav",
            "resources/sound/fest/clarinet.wav",
            "resources/sound/fest/drum1.wav",
>>>>>>> Stashed changes
            "resources/sound/fest/drums2.wav",
            "resources/sound/fest/drums3.wav",
            "resources/sound/fest/guitar1.wav",
            "resources/sound/fest/harp1.wav",
            "resources/sound/fest/idkwhatthisis1.wav",
<<<<<<< Updated upstream
            "resources/sound/fest/rtm.wav",
=======
            "resources/sound/fest/drum4s.wav",
>>>>>>> Stashed changes
            "resources/sound/fest/synth1.wav",
        ]

        for row in range(4):  
            for col in range(4):  
                top_left = (start_y + row * self.tile_size, start_x + col * self.tile_size)
                bottom_right = (top_left[0] + self.tile_size - 1, top_left[1] + self.tile_size - 1)
<<<<<<< Updated upstream
                sound_path = sound_filepaths[tile_id - 1]
=======
                sound_path = SOUND_FILEPATHS[tile_id - 1]
>>>>>>> Stashed changes

                # Create or retrieve a FlyweightTile instance using the Flyweight pattern
                is_number_sequence_tile = tile_id in {1, 2, 3, 4}
                flyweight_tile = FlyweightTile(tile_id, top_left, bottom_right,sound_path,is_number_sequence_tile)
                self.tiles[(top_left, bottom_right)] = flyweight_tile  # Store the FlyweightTile instance

                tile_id += 1

    def check_player_position(self, player: Player) -> tuple[int | None, list[Message]]:
        """ Check if the player is inside an abstract tile and return the tile ID and messages. """
        player_position = player.get_current_position()
        player_pos_tuple = (player_position.y, player_position.x)  # Convert Coord to tuple
        tile_id = None
        sound_path = None
        matched_tile=None


        for (top_left, bottom_right), flyweight_tile in self.tiles.items():
            if (top_left[0] <= player_pos_tuple[0] <= bottom_right[0] and 
                top_left[1] <= player_pos_tuple[1] <= bottom_right[1]):
                tile_id = flyweight_tile.get_tile_id()
                sound_path = flyweight_tile.get_sound_filepath()
                matched_tile = flyweight_tile
        old_tile = self.current_tile_for_player.get(player.get_name(), None)
        if old_tile is not None and old_tile != matched_tile:
<<<<<<< Updated upstream
=======
            
>>>>>>> Stashed changes
            if old_tile.is_number_sequence_tile:
                old_tile.stored_sequence = []  
                print(f"DEBUG: Reset sequence for old tile {old_tile.tile_id} because player left it.")

       
        self.current_tile_for_player[player.get_name()] = matched_tile
<<<<<<< Updated upstream
        if matched_tile is not None:
            self.notify_tile_activation(matched_tile)


        return tile_id, matched_tile,sound_path
=======


        return tile_id, matched_tile,sound_path
>>>>>>> Stashed changes
