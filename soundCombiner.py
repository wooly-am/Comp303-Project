import wave
from enum import Enum

## also wav files should be 16bit, exact length.

## takes a server message or file? message

## Server message

## Add logic for this later.

CANCEL = False

FRAMERATE = 44100
SAMPLE_LENGTH = 2 * FRAMERATE

class SCStatus(Enum):
    IDLE = 0
    IN_PROGRESS = 1
    COMPLETE = 2

SCStatus(0)

## can be overridden in case we decide to do theme changes.
def get_timed_sequence(num) -> []:
    if num & 2:
        return [88200 // num] * num
    else:
        temp = [44100 / 4] * num
        temp.append(11025 * (8 - num))
        return temp

def parse(message) -> str:
    timed_sequence = get_timed_sequence(message.sequence.length)

    with wave.open(message.path, "rb") as sample, wave.open("resources/fest/"+ message.id + ".wav", "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(FRAMERATE)

        for i in timed_sequence.length:
            sample.setpos((2 * FRAMERATE * (message.sequence[i] - 1)))
            output.writeframes(sample.readframes(timed_sequence[i]))

    return message.id + ".wav"

#message stuff should be changed
def render(message: dict, cancel = CANCEL):

    if SCStatus != 2:
        cancel = True

    ## get files
    amplitudes = [0] * SAMPLE_LENGTH


    print(message)
    for i in range(int(message["len"])):
        try:
            if message[str(i)]["type"].equals("instrument"):
                path = parse(message[str(i)])
            else:
                path = message[str(i)]["path"]
                print("yoss")

            with wave.open(path, 'rb') as current:
                ## if instro -> render and return. if loop -> return path

                amplitudes += int.from_bytes(current.readframes(SAMPLE_LENGTH), 'little') / message["len"]

        except:
            ## send message back
            print("Files Not found")
            ## can call getsound if this is in the client.
            pass

    with wave.open("rsrc_cache/sound/fest/output.wav", mode="wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(FRAMERATE)

        output.writeframes(bytes(amplitudes))

def trash_concurrent_process(cancel = CANCEL):
    if cancel:
        cancel = False
        raise Warning("Sound Render Timeout")


if __name__ == '__main__':
    pass