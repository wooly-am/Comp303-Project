from ..imports import *
from abc import ABC

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from message import *

FRAMERATE = 44100
SAMPLE_LENGTH = FRAMERATE * 2


class FestSubMessage(ABC):


    @abstractmethod
    def get_id(self):
        pass

    def _get_data(self) -> dict[str:str]:
        pass


    ## wish we could use this, alas json is fickle. def parse(self) -> str:

class LoopMessage(FestSubMessage):

    def __init__(self, path: str, tile_id: int):
        self.__tile_id = tile_id
        self.__path = path
        print(self.__path)

    def get_id(self) -> int:
        return self.__tile_id

    def _get_data(self)-> dict[str:str]:
        return "loop," + str(self.__tile_id) + "," + self.__path
            ## must be a string, so will have to later break it up


class InstrumentMessage(FestSubMessage):
    def __init__(self, path, tile_id, sequence):
        print("INITIATING INSTRO")
        self.__path = path
        self.sequence = sequence
        self.__tile_id = tile_id

    def get_id(self):
        return self.__tile_id

    def _get_data(self)-> dict[str:str]:
        return "instrument," + str(self.__tile_id) + "," + self.__path + "," + str(self.sequence)

    def update_sequence(self, new_sequence):
        self.sequence = new_sequence


## hard-coded backing track

ambient = LoopMessage("sound/fest/backing_track.wav", -1)


class FestMessage(Message, SenderInterface):

    def __init__(self, recipient: RecipientInterface):
        super().__init__(self, recipient)
        ## alternate data structures:
        ## heap, hashmap (for checking)
        ## Composite had two functions: check if there has been a change, add/remove value,
        self.__children = []
        self.__length = 0
        self.dirty = False

        self.add(ambient)

    def __str__(self):
        ## add more to aid debugging
        return str(len(self.__children))

    def get_name(self) -> Literal['***SERVER***']:
        return "***SERVER***"

    def _get_data(self) -> dict[str, str]:
        temp = {"len": self.__length, "classname": "FestMessage"}

        ## init iterator
        i = 0

        for submessage in self.__children:
            # message entries have to be easily accessed, e.g. sequentially in sound combiner.
            # however they are not stored that way in fest_message

            ## Polymorphism does not work properly? Probably a problem with my limited python knowledge

            temp[str(i)] = submessage._get_data()

            print(i)
            i+=1

        print(temp)
        return temp

    def add_recipient(self, recipient: RecipientInterface) -> Message:
        copy = FestMessage(recipient)
        ## I lowkey don't care if this means children can be changed.
        copy.__children = self.__children
        copy.__length = self.__length

        return copy

    def remove_tile(self, tile_id: int):
        for i, submessage in enumerate(self.__children):
            if submessage.get_id() == tile_id:
                self.__children.pop(i)
                self.__length -= 1
                self.dirty = True
                break

    def length(self) -> int:
        return self.__length

    def make_dirty(self):
        self.dirty = True

    def add(self, child: FestSubMessage):
        new = True
        for existing in self.__children:
            if child.get_id() == existing.get_id():
                ## if the ids are the same, theyre the same type
                if isinstance(child, InstrumentMessage):
                    existing.update_sequence(child.sequence)
                new = False
                break
        if new:
            self.dirty = True
            self.__children.append(child)
            self.__length += 1


    def remove(self, child):
        self.dirty = True
        self.__children.remove(child)
        ## add checks. im not sure about the id system

    def clear(self):
        for key in self:
            self.remove(key)

    def __iter__(self):
        self.count = 0
        return self.__children[self.count]

    def __next__(self):
        if self.count >= self.__length:
            raise StopIteration
        self.count += 1
        return self.__children[self.count]