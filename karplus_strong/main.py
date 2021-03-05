import wave

import numpy

# Sampling rate
FRAME_RATE = 44100


def generate_note(freq, clip_length=1):
    nframes = FRAME_RATE * clip_length
    t = numpy.arange(nframes) / FRAME_RATE
    amp = numpy.sin(2 * numpy.pi * freq * t)
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
    wav = amp_to_wav(generate_note(220, 5))
    write_wav('sine220.wav', wav)


if __name__ == '__main__':
    main()
