from ..imports import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Player import HumanPlayer
    from command import ChatCommand
    from maps.base import Map
    from message import Message


class InstrumentCommand(ChatCommand):

    ## maybe all instrument logic should be here?

    @classmethod
    def matches(cls, command_text: str) -> bool:
        pass

    def execute(self, command_text: str, context: "Map", player: "HumanPlayer") -> list[Message]:
        pass
