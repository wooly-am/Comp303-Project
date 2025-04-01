## idek if we should still add the two modes (singleplayer and multi)
## Would require additional logic for player on/off

# composite has two types: instrument and loop

from fest_message import *

class Leaf:

    def __init__(self, loop):
        self.__data = loop


class Composite:

    def __init__(self):
        ## alternate data structures:
        ## heap, hashmap (for checking)
        ## Composite had two functions: check if there has been a change, add/remove value,
        self.__children = {}
        self.dirty = False

    def dirty(self):
        self.dirty = True

    def add(self, child):
        self.dirty = True
        self.__children[child.tile_id] = child

    def remove(self, child):
        self.dirty = True
        self.__children.pop(child.tile_id)
        ## add checks. im not sure about the id system

    def send_message(self):
        if self.dirty:
            new_message = FestMessage()
            for child in self.__children:
                new_message.append(child.__data.get_message_data())
                ## data is a fest submessage.
            self.dirty = False