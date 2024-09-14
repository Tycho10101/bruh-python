import os, sys
from PIL import Image

def hex_to_rgb(hex_color):
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}. Expected format: RRGGBB.")
    
    try:
        # Convert hex to RGB
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid characters in hex color: {hex_color}.")
    
def set_pixel_color(x, y, hex_color):
    rgb_color = hex_to_rgb(hex_color)
    img.putpixel((x, y), rgb_color)
    
def split_every_6_chars(string):
    return [string[i:i+6] for i in range(0, len(string), 6)]

bruhfile = open(sys.argv[1], "rb")
size = bruhfile.read(8)
bruh = bruhfile.read()
bruhfile.close()

width = size[0:4]
height = size[4:8]
width = int.from_bytes(width, byteorder=sys.byteorder)
height = int.from_bytes(height, byteorder=sys.byteorder)
size = (width, height)

bruh = str(bruh, encoding='utf-8').splitlines()
img = Image.new("RGB", size)

print("debruh-fing")
iy = 0
while iy < height:
    ix = 0
    while ix < width:
        hex = bruh[iy]
        hex = split_every_6_chars(hex)[ix - 1]
        set_pixel_color(ix - 1, iy, hex)
        ix += 1
    iy += 1

print("now showing")
img.show()
