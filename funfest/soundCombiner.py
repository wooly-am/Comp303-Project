import wave
from enum import Enum

from fest_message import *

## also wav files should be 16bit, exact length.

## takes a server message or file? message

## Server message

## Add logic for this later.

CANCEL = False

class SCStatus(Enum):
    IDLE = 0
    IN_PROGRESS = 1
    COMPLETE = 2

SCStatus(0)

#message stuff should be changed
def render(message: FestMessage, cancel = CANCEL):

    if SCStatus != 2:
        cancel = True

    ## get files
    amplitudes = [0] * SAMPLE_LENGTH

    for sub_message in message:
        try:
            with wave.open(sub_message.parse(), 'rb') as current:
                ## if instro -> render and return. if loop -> return path

                for sample in range(message.length()):
                    amplitudes += int.from_bytes(current.readframes(SAMPLE_LENGTH), 'little') / message.length()

                current.close()
        except:
            ## send message back
            pass

    with wave.open("output.wav", mode="wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(FRAMERATE)

        output.writeframes(bytes(amplitudes))
        output.close()

def trash_concurrent_process(cancel = CANCEL):
    if cancel:
        cancel = False
        raise Warning("Sound Render Timeout")

