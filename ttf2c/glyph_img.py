#
# Copyright (c) 2023 by Vasilii Tsarevkii
#
# See the README and LISENSE files for information on usage and redistribution.
#

from PIL import Image
import numpy
import rpack
import math
import os


def draw_glyphs(glyphs: numpy.array, path: str, spaces: int = 1, inverse: bool = False):
    sizes = []
    glyphs_area = 0

    glyph_line = numpy.full(shape=(glyphs[0].shape[0], 0), fill_value=inverse, dtype=bool)
    spacer = numpy.full(shape=(glyphs[0].shape[0], spaces), fill_value=inverse, dtype=bool)

    for i, glyph in enumerate(glyphs):
        # Draw single glyph img
        im = Image.fromarray(glyph)
        fp = os.path.join(path, f"glyph_{i}.png")
        im.save(fp)

        # create list of glyph sizes with offset
        glyphs_area += (glyph.shape[0] + 2 * spaces) * (glyph.shape[1] + 2 * spaces)
        sizes.append((glyph.shape[1] + 2 * spaces, glyph.shape[0] + 2 * spaces))

        # create glyphs array in one line
        glyph_line = numpy.concatenate((glyph_line, spacer, glyph), axis=1)

    length_of_edge = math.ceil(math.sqrt(glyphs_area))
    positions = rpack.pack(sizes, length_of_edge, length_of_edge * 2)

    size_x, size_y = rpack.bbox_size(sizes, positions)
    glyph_map = numpy.full(shape=(size_y, size_x), fill_value=inverse, dtype=bool)

    for i, (x, y) in enumerate(positions):
        glyph = glyphs[i]
        glyph_size_x = glyph.shape[1]
        glyph_size_y = glyph.shape[0]
        glyph_map[(y + spaces):(y + glyph_size_y + spaces), (x + spaces):(x + glyph_size_x + spaces)] = glyph

    im = Image.fromarray(glyph_map)
    fp = os.path.join(path, "glyph_map.png")
    im.save(fp)

    im = Image.fromarray(glyph_line)
    fp = os.path.join(path, "glyph_line.png")
    im.save(fp)
