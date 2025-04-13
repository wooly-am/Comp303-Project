from ..imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import HumanPlayer
    from command import ChatCommand
    from maps.base import Map
    from message import Message, ServerMessage

class ClearSequence(ChatCommand):
    name: str = "clear"
    desc: str = "Clears the sequence for the instrument tile"

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text == ""

    def execute(self, command_text: str, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages = []

        tile_id, tile, _ = None, None, None

        if hasattr(context, 'tile_map'):
            result = context.tile_map.check_player_position(player)
            if result:
                tile_id, tile, _ = result

        if tile and tile.is_number_sequence_tile:
            tile.clear_sequence()
            if not tile.get_stored_sequence:
                messages.append(ServerMessage(player, f"Successfully cleared tile {tile_id}'s sequence!"))
            else:
                messages.append(ServerMessage(player, f"Unsuccess."))
        return messages

class AddToSequence(ChatCommand):
    name: str = "add"

    ## maybe all instrument logic should be here?

    @classmethod
    def matches(cls, command_text: str) -> bool:
        return command_text.isdigit() and ("0" <= command_text <= "8")

    def execute(self, command_text: str, context: "Map", player: "HumanPlayer") -> list[Message]:
        messages = []

        tile_id, tile, _ = None, None, None

        if hasattr(context, 'tile_map'):
            result = context.tile_map.check_player_position(player)
            if result:
                tile_id, tile, _ = result

        if tile and tile.is_number_sequence_tile:
            if command_text.isdigit():
                number = int(command_text)
                if 1 <= number <= 8:
                    tile.store_number(number)
                    messages.append(ServerMessage(player, f"You entered {number}; tile {tile_id} sequence: {tile.get_stored_sequence()}"))
                else:
                    messages.append(ServerMessage(player, "Invalid. Enter 1-8."))

        return messages