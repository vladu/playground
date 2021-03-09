import argparse

import numpy
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps


CHARS_COARSE = '@%#*+=-:. '
CHARS_FINE = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def compute_tiles(w, h, cols, font_aspect_ratio):
    if cols > w:
        raise ValueError('Image too small. It is only {} pixels wide, but requested {} cols in output'.format(w, cols))

    tile_w = w / cols
    tile_h = tile_w / font_aspect_ratio
    rows = h // tile_h

    if rows < 1:
        raise ValueError(
            'Image too small. For tile width {} and font aspect ratio {}, must be at least {} pixels high, '
            'but is actually only {} pixels'.format(int(tile_w), font_aspect_ratio, int(tile_h), h)
        )

    return int(tile_w), int(tile_h), int(rows)


def generate_tile_dims(w, h, rows, cols, tile_w, tile_h):
    for r in range(rows):
        y0 = r * tile_h
        y1 = h if r == rows - 1 else (y0 + tile_h)
        for c in range(cols):
            x0 = c * tile_w
            x1 = w if c == cols - 1 else (x0 + tile_w)
            yield x0, y0, x1, y1


def compute_scales(img, w, h, rows, cols, tile_w, tile_h):
    tile_dims = generate_tile_dims(w, h, rows, cols, tile_w, tile_h)
    tiles = (img.crop((x0, y0, x1, y1)) for x0, y0, x1, y1 in tile_dims)
    tile_scales = (numpy.average(numpy.array(tile)) for tile in tiles)
    return numpy.array(list(tile_scales)).reshape((rows, cols))


def gray_scales_to_ascii(scales, char_arr):
    char_scales = numpy.round(scales / 255 * (len(char_arr) - 1)).astype(int)
    chars = numpy.asarray(list(char_arr))[char_scales]
    return '\n'.join(''.join(r) for r in chars)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-c', '--cols', type=int, default=80)
    parser.add_argument('-r', '--font-aspect', dest='font_aspect_ratio', type=float, default=0.43)
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-f', '--fine', dest='fine_scale', default=False, action='store_true')
    parser.add_argument('-o', '--output')
    return parser.parse_args()


def main():
    options = _parse_args()

    with Image.open(options.file) as img:
        img = ImageOps.grayscale(img)

        w, h = img.size
        cols = options.cols
        tile_w, tile_h, rows = compute_tiles(w, h, cols, options.font_aspect_ratio)
        scales = compute_scales(img, w, h, rows, cols, tile_w, tile_h)

        if options.debug:
            draw = ImageDraw.Draw(img)
            flat_scales = scales.reshape(rows * cols)
            for idx, (x0, y0, x1, y1) in enumerate(generate_tile_dims(w, h, rows, cols, tile_w, tile_h)):
                draw.rectangle((x0, y0, x1, y1), fill=int(flat_scales[idx]), outline=0)
            img.show()

        art = gray_scales_to_ascii(scales, CHARS_FINE if options.fine_scale else CHARS_COARSE)
        if options.output is None:
            print(art)
        else:
            with open(options.output, 'w') as f:
                print(art, file=f)


if __name__ == '__main__':
    main()
