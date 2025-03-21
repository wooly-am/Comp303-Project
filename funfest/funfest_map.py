from coord import Rect
from maps.base import Map
from tiles.base import MapObject
from tiles.map_objects import *
from maps.map_helper import fill_area
from tileMap import TileMap
from Player import Player, HumanPlayer
from tiles.map_objects import Computer
from drugfest.instrument_command import *
from server_local import ChatBackend
from queue import Queue

# multiple of 2!!:
roomWidth = 36
roomHeight = 40
original_parse_message = ChatBackend._ChatBackend__parse_message

def funfest_parse_message(self, data_d, player):
    """Custom parse method to read user’s chat input for number-sequence tiles."""
    print("FunFestHouse override parse_message:", data_d)

    messages = []

    try:
        if 'text' in data_d:
            chat_text = data_d['text']

            
            tile_id, tile, _ = None, None, None
            current_room = player.get_current_room()
            if hasattr(current_room, 'tile_map'): 
                result = current_room.tile_map.check_player_position(player)
                if result:
                    tile_id, tile, _ = result

            
            if tile and tile.is_number_sequence_tile:
                if chat_text.isdigit():
                    number = int(chat_text)
                    if 1 <= number <= 8:
                        tile.store_number(number)
                        messages.append(ServerMessage(player, f"You entered {number}; tile {tile_id} sequence: {tile.get_stored_sequence()}"))
                    else:
                        messages.append(ServerMessage(player, "Invalid. Enter 1-8."))
                else:
                    ## instrument command will handle if the text is not a digit, checking for commands like clear, etc
                    messages.append(InstrumentCommand().execute(player, self, data_d))
                    #messages.append(ServerMessage(player, "Enter a valid number (1-8)."))
            else:
                
                original_parse_message(self, data_d, player)
                return  

        else:
            
            original_parse_message(self, data_d, player)
            return

    except Exception as e:
        messages = [ServerMessage(player, f"Error in funfest_parse_message: {str(e)}")]

    self._ChatBackend__send_messages_to_recipients(messages)
class FunFestHouse(Map):
    def __init__(self) -> None:
        super().__init__(
            name="FunFestHouse",
            description="Project test..",
            size=(roomHeight, roomWidth),
            entry_point=Coord(30, 10),
            background_tile_image='cobblestone',
            chat_commands=[],
            
            
        )
        self.placed_objects = []
        self.tile_map=TileMap(10,10,4)
        ChatBackend._ChatBackend__parse_message = funfest_parse_message
    

    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        door = Door('int_entrance', linked_room="Trottier Town")
        objects.append((door, Coord(roomHeight - 1, (roomWidth // 2) - 1)))
        background = MapObject('tile/background/black', False, 2)
        for x in range(roomWidth):
            for y in range(roomHeight):
                if not ((((roomWidth // 2) - 2 <= x <= (roomWidth // 2) + 1) and (roomWidth - 10 <= y <= roomHeight)) or ((10 <= x <= roomWidth - 11) and (10 <= y <= roomWidth - 11))):
                    objects.append((background, Coord(y,x)))
        return objects
    

 
    def move(self, player: "Player", direction_s: str) -> list[Message]:
        """
        Move the player, check tile type, and handle number-sequence input.
        """
        
        messages = super().move(player, direction_s)

        
        tile_id, tile, _ = self.tile_map.check_player_position(player)

        
        if tile_id is not None:
            messages.append(ServerMessage(player, f"DEBUG: Player {player.get_name()} is in Tile {tile_id}"))

            
            if tile.is_number_sequence_tile:
                messages.append(ServerMessage(player, "Enter a number (1-8) in chat."))

                
        return messages

    

    



    






    def check_player_position(self, player: Player):
        """  Check if player is inside a tile and activate the effect. """
        self.tile_map.check_player_position(player) 


    def clear_board(self):
        # remove all squares from 10,10 to 12,12.
        for obj, coord in self.placed_objects:
            self.remove_from_grid(obj, coord)
