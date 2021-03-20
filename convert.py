#!/usr/bin/env python3
import os, sys, io, shutil
from PIL import Image

DISPLAY_RESOLUTION = (400, 300)

COLOR_WHITE = 0
COLOR_RED = 1
COLOR_BLACK = 2

for infile in sys.argv[1:]:
    filename, ext = os.path.splitext(infile)
    filename = os.path.basename(filename)

    black_array = []
    red_array = []

    with Image.open(infile) as im:
        if (im.size != DISPLAY_RESOLUTION):
            print("Image resolution does not match display resolution")
            exit(2)
        px = im.load()
        blackImg = Image.new('L', im.size)
        redImg = Image.new('L', im.size)
        i = 7
        blackByte = 0
        redByte = 0
        for y in range(0, im.size[1]):
            for x in range(0, im.size[0]):

                if px[x, y] == COLOR_BLACK:
                    blackByte |= 1 << i
                    redByte |= 1 << i
                elif px[x, y] == COLOR_RED:
                    blackByte |= 0
                    redByte |= 0
                else:
                    blackByte |= 0
                    redByte |= 1 << i

                if i == 0:
                    black_array.append(blackByte)
                    red_array.append(redByte)
                    blackByte = 0
                    redByte = 0
                    i = 7
                else:
                    i -= 1

                # Write pixels
                if px[x, y] == COLOR_BLACK:
                    blackImg.putpixel((x, y), 255)
                    redImg.putpixel((x, y), 255)
                elif px[x, y] == COLOR_RED:
                    blackImg.putpixel((x, y), 0)
                    redImg.putpixel((x, y), 0)
                else:
                    blackImg.putpixel((x, y), 0)
                    redImg.putpixel((x, y), 255)

    # Construct black image
    black_string = "const unsigned char gImage_4in2bc_b[] = {"

    for px in black_array:
        black_string += "0x{:02x},".format(px)
    
    black_string = black_string.rstrip(',') + "};\n"

    # Construct red image
    red_string = "const unsigned char gImage_4in2bc_ry[] = {"

    for px in red_array:
        red_string += "0x{:02x},".format(px)
    
    red_string = red_string.rstrip(',') + "};"

    # Cleanup
    if not os.path.exists('output'):
        os.mkdir('output')
    if (os.path.exists('output/' + filename)):
        shutil.rmtree('output/' + filename)
    os.mkdir('output/' + filename)
    shutil.copy(infile, 'output/' + filename + '/original' + ext)
    

    # Write images
    blackImg.save('output/' + filename + '/' + 'black.bmp')
    redImg.save('output/' + filename + '/' + 'red.bmp')

    # Write file
    f = open('output/' + filename + '/' + 'output.c', 'w')
    f.write("#include \"ImageData.h\"\n\n" + black_string + red_string)
    f.close()