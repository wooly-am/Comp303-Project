import wave
import struct
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
    ## probably wouldn't make sense to redefine the message data structure here so remember indexes:
    ## 0 -> type. 1 -> id. 2 -> path. 3-> sequence

    timed_sequence = get_timed_sequence(len(message[3]))

    with wave.open(message[2], "rb") as sample, wave.open("resources/fest/"+ message[1] + ".wav", "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(FRAMERATE)

        for i in timed_sequence.length:
            sample.setpos((2 * FRAMERATE * (message[3][i] - 1)))
            output.writeframes(sample.readframes(timed_sequence[i]))

    return message[1] + ".wav"


def render(message: dict, cancel = CANCEL):

    if SCStatus != 2:
        cancel = True

    ## get files
    amplitudes = [0] * SAMPLE_LENGTH

    for i in range(int(message['len'])):
        submessage = message[str(i)].split(",")

        try:
            if submessage[0] == "instrument":
                path = parse(submessage)
            else:
                path = submessage[2]
                path = "rsrc_cache/" + path[13:]
                print(path)

            with wave.open(path, 'rb') as current:
                ## if instro -> render and return. if loop -> return path

                cur_frame = struct.unpack("<" + "i" * SAMPLE_LENGTH, current.readframes(SAMPLE_LENGTH))
                amplitudes = [sum(pair) for pair in zip(amplitudes, cur_frame)]

            max_val = max(abs(sample) for sample in amplitudes)
            if max_val > 32767:
                amplitudes = [int(sample * 32767 / max_val) for sample in amplitudes]

            ##print(amplitudes)

        except FileNotFoundError:
            ## send message back
            print("Files Not found")
            ## can call getsound if this is in the client.
            pass


    packed_frames = [struct.pack("<h", sample) for sample in amplitudes]

    with wave.open("rsrc_cache/sound/fest/output.wav", mode="wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(FRAMERATE)

        output.writeframes(b''.join(packed_frames))

def trash_concurrent_process(cancel = CANCEL):
    if cancel:
        cancel = False
        raise Warning("Sound Render Timeout")


if __name__ == '__main__':
    pass