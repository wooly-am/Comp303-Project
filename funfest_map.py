from .imports import *
from .funfest.tileMap import TileMap, FlyweightTile, SOUND_FILEPATHS
from .funfest.fest_message import FestMessage, InstrumentMessage, LoopMessage
from .funfest.instrument_command import InstrumentCommand

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from coord import Coord
    from message import Message
    from maps.base import Map
    from tiles.map_objects import Door, Background, MapObject
    from message import ServerMessage, SoundMessage
    from Player import Player
    from server_local import ChatBackend


DIRECTORY = [
    "/fest/backing_track.wav"
]


# multiple of 2!!:
roomWidth = 36
roomHeight = 40
original_parse_message = ChatBackend._ChatBackend__parse_message


#@override
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

    MAIN_ENTRANCE = True

    clock_two = False

    def __init__(self) -> None:
        super().__init__(
            name="FunFestHouse",
            description="Project test..",
            size=(roomHeight, roomWidth),
            entry_point=Coord(roomHeight - 1, (roomWidth // 2) - 1),
            background_tile_image='black',
            chat_commands=[],


        )
        self.placed_objects = []
        self.tile_map=TileMap(10,10,4)
        self.active_tiles = FestMessage(self)
        ChatBackend._ChatBackend__parse_message = funfest_parse_message
        self.tile_map.add_observer(self)
        self.player_load_queue = []
        self.observers = []
        self.sequence_store = [[],[],[],[]]

    def on_tile_activated(self, tile):
        if tile.sound_path and tile.get_tile_id() >= 1:

            if tile.is_number_sequence_tile:
                #messages.append(ServerMessage(player, "Enter a number (1-8) in chat."))
                self.active_tiles.add(InstrumentMessage(tile.get_sound_filepath(), tile.get_tile_id(), "".join(str(item) for item in tile.get_stored_sequence()) ))
            else:
                self.active_tiles.add(LoopMessage(tile.get_sound_filepath(), tile.get_tile_id()))

    def on_sequence_update(self, tile):
        self.active_tiles.add(InstrumentMessage(tile.get_sound_filepath(), tile.get_tile_id(), "".join(str(item) for item in tile.get_stored_sequence())))


    def get_objects(self) -> list[tuple[MapObject, Coord]]:
        objects: list[tuple[MapObject, Coord]] = []
        door = Door('int_entrance', linked_room="Trottier Town", is_main_entrance=True)
        objects.append((door, Coord(14, 7)))

        background = MapObject('tile/background/cobblestone', True, 10)
        for x in range(roomWidth):
            for y in range(roomHeight):
                if (((roomWidth // 2) - 2 <= x <= (roomWidth // 2) + 1) and (roomWidth - 10 <= y <= roomHeight)) or ((10 <= x <= roomWidth - 11) and (10 <= y <= roomWidth - 11)):
                    if y > 25:
                        objects.append((background, Coord(y,x)))

        for i in range(6):
            for j in range(7):
                path = str("tile/background/festgrid/row-"+ str(i+1) +"-column-" + str(j+1))
                objects.append((MapObject(path, True, 7), Coord( ((4*i)+2), ((4*j)+2) )))

        ## background imagery:
        objects.append((MapObject("fest-foreground", True, 0), Coord(23,3)))

        return objects



    def update(self):
        messages = []
        self.clock_two = not self.clock_two


        ## holy shit this code needs to be cleaned. It just needs to work rn tho.
        for player in self.get_clients():

            if player in self.player_load_queue:
                for path in SOUND_FILEPATHS:
                    messages.append(SoundMessage(player, path[6:], 0.0))


                messages.append(self.active_tiles.add_recipient(player))
                self.player_load_queue.remove(player)
            elif self.active_tiles.dirty and self.clock_two:
                #print("Sending Fest_message", self.active_tiles)
                messages.append(self.active_tiles.add_recipient(player))

            elif self.active_tiles.dirty:
                #print("Playing sound")
                messages.append(SoundMessage(player,"fest/output.wav", 0.5))

            tile_id , tile, _ = self.tile_map.check_player_position(player)
            if tile_id in {1,2,3,4}:
                self.active_tiles.add(InstrumentMessage(tile.get_sound_filepath(), tile.get_tile_id(), "".join(str(item) for item in tile.get_stored_sequence())))

        return messages




    def add_player(self, player: "Player", entry_point = None) -> None:


        self.active_tiles.make_dirty()
        self.player_load_queue.append(player)


        Map.add_player(self, player, entry_point)




    #@override
    def move(self, player: "Player", direction_s: str) -> list[Message]:
        """
        Move the player, check tile type, and handle number-sequence input.
        """

        messages = super().move(player, direction_s)



        tile_id, tile, _ = self.tile_map.check_player_position(player)




        if tile_id is not None:
            messages.append(ServerMessage(player, f"DEBUG: Player {player.get_name()} is in Tile {tile_id}"))

            print(tile.is_number_sequence_tile)
            print(tile_id)

        return messages


    def check_player_position(self, player: Player):
        """  Check if player is inside a tile and activate the effect. """
        self.tile_map.check_player_position(player)


    def clear_board(self):
        # remove all squares from 10,10 to 12,12.
        for obj, coord in self.placed_objects:
            self.remove_from_grid(obj, coord)
    def remove_tile_loop(self, tile: FlyweightTile, player: Player):
        """
        Called when `player` leaves `tile`
        """
        tile_id = tile.get_tile_id()

        self.active_tiles.remove_tile(tile_id)
        print(f"Removed loop for tile {tile_id} because {player.get_name()} left it.")


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


    def add_observer(self, callback):
        self.observers.append(callback)