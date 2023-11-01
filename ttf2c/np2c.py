#
# Copyright (c) 2023 by Vasilii Tsarevkii
#
# See the README and LISENSE files for information on usage and redistribution.
#

import os


def var_size(value):
    for i in [8, 16, 32, 64]:
        if value.bit_length() < i:
            return i


def array_element(element, comment):
    return f"    {element:#04x}{comment}"


def array_wrap(data_type: str, pointer: str, content: str):
    return f"static const {data_type} {pointer}[] = {{\n" + content + "};\n\n"


def generate_c_file(font_name,
                    output_path,
                    mono,
                    char_set,
                    bitmaps_pack,
                    bitmaps,
                    baseline_px,
                    max_height_px,
                    max_width_px,
                    kerning_px,
                    space_width_px):

    # Init vars to determine the size of С variables
    max_glyph_value = 0
    offset = 0
    bitmap_array_size = 0

    # Array strings
    charmap_string = ""
    bitmap_string = ""
    offset_string = ""
    width_string = ""

    # Fill array strings and size variables
    for i, glyph_id in enumerate(char_set):
        # Create universal comment:
        comment_short = f"{i}, '{chr(glyph_id)}' "
        comment = f", //{comment_short} \n"

        # Char map
        max_glyph_value = max(glyph_id, max_glyph_value)
        charmap_string += array_element(glyph_id, comment)

        # Offset + width
        if not mono:
            offset_string += array_element(offset, comment)
            width_string += array_element(bitmaps[i].shape[1], comment)

            offset += bitmaps_pack[i].size

        # Bitmap
        bitmap_array_size += bitmaps_pack[i].size
        # Write glyph representation by ascii art in comment
        bitmap_string += f"//Char {comment_short}size:{bitmaps_pack[i].shape[1]}x{bitmaps_pack[i].shape[0]}\n"
        for x in bitmaps[i]:
            bitmap_string += f'//'
            for y in x:
                if y:
                    bitmap_string += f'▀'
                else:
                    bitmap_string += f'.'
            bitmap_string += f'\n'

        # Write glyph array
        for x in bitmaps_pack[i]:
            bitmap_string += f"    "
            for y in x:
                bitmap_string += f"{y:#04x}, "
            bitmap_string += '\n'
        bitmap_string += '\n'

    # Create variables types
    glyph_num = len(char_set)
    glyph_index_bits = var_size(glyph_num.bit_length())

    charmap_bits = var_size(max_glyph_value)
    charmap_bytes = (charmap_bits // 8) * len(bitmaps_pack)

    offset_bits = var_size(offset)
    offset_bytes = (charmap_bits // 8) * len(bitmaps_pack)

    width_bytes = len(bitmaps_pack)

    glyphi_t = f"uint{glyph_index_bits}_t"
    charmap_t = f"uint{charmap_bits}_t"
    offs_t = f"uint{offset_bits}_t"

    # Create array(pointers) names
    charmap_p = f"{font_name}_charmap"
    offset_p = f"{font_name}_offset"
    width_p = f"{font_name}_width"
    bitmap_p = f"{font_name}_bitmap"

    # Wrap arrays
    charmap_string = array_wrap(charmap_t, charmap_p, charmap_string)
    bitmap_string = array_wrap("uint8_t", bitmap_p, bitmap_string)
    offset_string = array_wrap(offs_t, offset_p, offset_string)
    width_string = array_wrap("uint8_t", width_p, width_string)


    if mono:
        offset_bytes = 0
        width_bytes = 0

        offs_t = f"uint8_t"
        offset_string = ""
        width_string = ""
        offset_p = "(void*)0"
        width_p = "(void*)0"


    # Create output file
    template = \
    "/******************************************************************************\n" \
     "*\n" \
    f"* Created by ttf2c converter.\n" \
     "* https://github.com/insane-person/ttf2c\n" \
     "*\n" \
    f"* Font: {font_name}\n" \
     "*\n" \
    f"* Size of glyph map array: {charmap_bytes} byte(s)\n" \
    f"* Size of width array:  {width_bytes} byte(s)\n" \
    f"* Size of offset array: {offset_bytes} byte(s)\n" \
    f"* Size of bitmap array: {bitmap_array_size} byte(s)\n" \
     "******************************************************************************/\n" \
     "#include <stdint.h>\n" \
     "\n"\
    f"typedef {charmap_t} charmap_t;\n" \
    f"typedef {offs_t} offs_t;\n" \
    f"typedef {glyphi_t} glyphi_t;\n" \
     "\n"\
     "typedef struct {\n"\
     "    charmap_t const* charmap;\n"\
     "    offs_t const* offset;\n"\
     "    uint8_t const* width;\n"\
     "    uint8_t const* bitmap;\n"\
     "    glyphi_t glyph_num;\n"\
     "    uint8_t baseline;\n"\
     "    uint8_t height;\n"\
     "    uint8_t mono;\n"\
     "    uint8_t max_width;\n"\
     "    uint8_t kerning;\n"\
     "    uint8_t space;\n"\
     "} font_t;\n"\
     "\n"\
    f"{charmap_string}" \
    f"{offset_string}" \
    f"{width_string}" \
    f"{bitmap_string}" \
    f"const font_t {font_name}_font = {{\n" \
    f"    .charmap = {charmap_p},\n" \
    f"    .offset = {offset_p},\n" \
    f"    .width = {width_p},\n" \
    f"    .bitmap = {bitmap_p},\n" \
    f"    .glyph_num = {glyph_num},\n" \
    f"    .baseline = {baseline_px},\n" \
    f"    .height = {max_height_px},\n" \
    f"    .mono = {int(mono)},\n" \
    f"    .max_width = {max_width_px},\n" \
    f"    .kerning = {kerning_px},\n" \
    f"    .space = {space_width_px}\n" \
     "};\n" \
     "\n"

    file_name = os.path.splitext(font_name)[0] + '.c'
    path = os.path.join(output_path, file_name)

    # Save to file
    f = open(path, "w", encoding='utf-8')
    f.write(template)
    f.close()

    # print statistics
    print(f"Glyph number: {len(char_set)}")
    print(f"Baseline: {int(baseline_px)} px")
    print(f"Max height: {int(max_height_px)} px")
    print(f"Max width: {int(max_width_px)} px")
    print(f"Size of glyph map array: {charmap_bytes} byte(s)")
    print(f"Size of width array:  {width_bytes} byte(s)")
    print(f"Size of offset array: {offset_bytes} byte(s)")
    print(f"Size of bitmap array: {bitmap_array_size} byte(s)")
    print(f"Overal size: {charmap_bytes + width_bytes + offset_bytes + bitmap_array_size} byte(s)")