import wave
from collections import deque

import numpy

# Sampling rate
FRAME_RATE = 44100


def generate_fundamental_note(freq, clip_length=1):
    nframes = FRAME_RATE * clip_length
    t = numpy.arange(nframes) / FRAME_RATE
    amp = numpy.sin(2 * numpy.pi * freq * t)
    return amp


def generate_ks_note(freq, clip_length=1, attenuation=0.996):
    def _gen_data():
        nframes = FRAME_RATE * clip_length
        buf = deque(numpy.random.rand(int(FRAME_RATE / freq)) - 0.5)
        for _ in range(nframes):
            data_point = buf.popleft()
            buf.append(attenuation * (data_point + buf[0]) / 2)
            yield data_point

    amp = numpy.array(list(_gen_data()))
    return amp


def amp_to_wav(amp):
    return (amp * numpy.iinfo(numpy.int16).max).astype(numpy.int16).tobytes()


def write_wav(fname, wav):
    with wave.open(fname, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(FRAME_RATE)
        f.setnframes(len(wav))
        f.setcomptype('NONE', 'uncompressed')

        f.writeframes(wav)


def main():
    #wav = amp_to_wav(generate_fundamental_note(220, 5))
    wav = amp_to_wav(generate_ks_note(262, 1))
    write_wav('ks262.wav', wav)


if __name__ == '__main__':
    main()
