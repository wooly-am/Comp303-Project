from abc import abstractmethod, ABC
import wave
from typing import Dict, Any

from message import *

FRAMERATE = 44100
SAMPLE_LENGTH = FRAMERATE * 2


class FestSubMessage(ABC):

    @abstractmethod
    def get_id(self):
        pass

    ## wish we could use this, alas json is fickle. def parse(self) -> str:

class LoopMessage(FestSubMessage):

    def __init__(self, path: str, tile_id: int):
        self.__tile_id = tile_id
        self.__path = path

    def get_id(self):
        return self.__tile_id

    def get_data(self)-> dict[str:str]:
        return "loop," + str(self.__tile_id) + "," + self.__path
            ## must be a string, so will have to later break it up


class InstrumentMessage(FestSubMessage):
    def __init__(self, path, tile_id, sequence):
        self.__path = path
        self.sequence = sequence
        self.__tile_id = tile_id

    def get_id(self):
        return self.__tile_id

    def get_data(self)-> dict[str:str]:
        return "instrument," + str(self.__tile_id) + "," + self.__path + "," + str(self.sequence)



## hard-coded backing track

ambient = LoopMessage("../resources/sound/fest/backing_track.wav", -1)


class FestMessage(Message, SenderInterface):

    #def __init__(self):
    #    self.__messages = []
    #    self.__length = 0

    #def append(self, message_data: FestSubMessage):
    #    return

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
        print("We're getting that data mfer")
        temp = {"len": self.__length, "classname": "FestMessage"}

        ## init iterator
        i = 0

        for submessage in self.__children:
            # message entries have to be easily accessed, e.g. sequentially in sound combiner.
            # however they are not stored that way in fest_message

            temp[str(i)] = self.__children[submessage.get_id()].get_data()
            print(temp[str(i)])
            i+=1
        return temp

    def add_recipient(self, recipient: RecipientInterface) -> Message:
        copy = FestMessage(recipient)
        ## I lowkey don't care if this means children can be changed.
        copy.__children = self.__children
        copy.__length = self.__length

        return copy


    def length(self) -> int:
        return self.__length

    def make_dirty(self):
        self.dirty = True

    def add(self, child: FestSubMessage):
        self.dirty = True
        self.__children.append(child)
        self.__length += 1

    def remove(self, child):
        self.dirty = True
        self.__children.pop(child.tile_id)
        ## add checks. im not sure about the id system

    def clear(self):
        for key in self:
            self.remove(key)

    #def send_message(self):
        ## this should maybe go
        #if self.dirty:
        #    new_message = FestMessage()
        #    for child in self.__children:
        #        new_message.add(child.__data.get_message_data())
       #         ## data is a fest submessage.
        #    self.dirty = False

    def __iter__(self):
        self.count = 0
        return self.__children[self.count]

    def __next__(self):
        if self.count >= self.__length:
            raise StopIteration
        self.count += 1
        return self.__children[self.count]