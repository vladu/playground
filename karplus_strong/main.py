
# Sampling rate
import os
import wave
from matplotlib import pyplot as plt

import numpy

FRAME_RATE = 44100


def main(clip_length=5):
    nframes = FRAME_RATE * clip_length
    sound_freq = 220.

    t = numpy.arange(nframes) / FRAME_RATE
    amp = numpy.sin(2 * numpy.pi * sound_freq * t)
    amp16 = (amp * numpy.iinfo(numpy.int16).max).astype(numpy.int16)

    # plt.plot(t[:1000], amp16[:1000])
    # plt.show()

    with wave.open('sine220.wav', 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(FRAME_RATE)
        f.setnframes(len(amp16))
        f.setcomptype('NONE', 'uncompressed')

        f.writeframes(amp16.tobytes())


if __name__ == '__main__':
    main()
