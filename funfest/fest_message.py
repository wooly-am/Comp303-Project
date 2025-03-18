from abc import abstractmethod, ABC
import wave
from message import *

FRAMERATE = 44100
SAMPLE_LENGTH = FRAMERATE * 2

## can be overridden in case we decide to do theme changes.
def get_timed_sequence(num) -> []:
     if num & 2:
         return [88200 // num] * num
     else:
         temp = [44100 / 4] * num
         temp.append(11025 * (8 - num))
         return temp


class FestSubMessage(ABC):

    @abstractmethod
    def get_id(self):
        pass

    def parse(self):
        pass

class LoopMessage(FestSubMessage):

    def __init__(self, path, id):
        self.__tile_id = id
        self.__path = path

    def get_id(self):
        return self.__tile_id

    def parse(self):
        pass

class InstrumentMessage(FestSubMessage):
    def __init__(self, path, id, sequence):
        self.__path = path
        self.sequence = sequence
        self.__tile_id = id

    def get_id(self):
        return self.__tile_id

    def parse(self):
        timed_sequence = get_timed_sequence(self.sequence.length)

        with wave.open(self.__path, "rb") as sample, wave.open(self.id, "wb") as output:
            output.setnchannels(1)
            output.setsampwidth(2)
            output.setframerate(FRAMERATE)

            for i in timed_sequence.length:
                sample.setpos((2 * FRAMERATE * (self.sequence[i] - 1)))
                output.writeframes(sample.readframes(timed_sequence[i]))

            sample.close()
            output.close()



## hard-coded backing track

ambient = LoopMessage("backing_track.wav", -1)


class FestMessage(Message):

    #def __init__(self):
    #    self.__messages = []
    #    self.__length = 0

    #def append(self, message_data: FestSubMessage):
    #    return

    def __init__(self, sender: SenderInterface, recipient: RecipientInterface):
        super().__init__(sender, recipient)
        ## alternate data structures:
        ## heap, hashmap (for checking)
        ## Composite had two functions: check if there has been a change, add/remove value,
        self.__children = {}
        self.__length = 0
        self.dirty = False

        self.add(ambient)

    def length(self) -> int:
        return self.__length

    def dirty(self):
        self.dirty = True

    def add(self, child: FestSubMessage):
        self.dirty = True
        self.__children[child.get_id()] = child

    def remove(self, child):
        self.dirty = True
        self.__children.pop(child.tile_id)
        ## add checks. im not sure about the id system

    def clear(self):
        for key in self:
            self.remove(key)

    def send_message(self):
        ## this should maybe go
        if self.dirty:
            new_message = FestMessage()
            for child in self.__children:
                new_message.add(child.__data.get_message_data())
                ## data is a fest submessage.
            self.dirty = False

    def __iter__(self):
        self.count = 0
        return self.__children[self.count]

    def __next__(self):
        if self.count >= self.__length:
            raise StopIteration
        self.count += 1
        return self.__children[self.count]
