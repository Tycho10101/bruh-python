import os, sys
from PIL import Image

def get_pixel_hex(x, y):
    r, g, b = img.getpixel((x, y))
    hex_value = "{:02x}{:02x}{:02x}".format(r, g, b)
    
    return hex_value

for infile in sys.argv[1:]:
    f, e = os.path.splitext(infile)
    outfile = f + ".bmp"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.save(outfile)
        except OSError:
            print("cannot convert", infile)
print("converted to bmp")
img = Image.open(outfile)
img = img.convert('RGB')

width, height = img.size

bwidth = width.to_bytes(length=4, byteorder=sys.byteorder)
bheight = height.to_bytes(length=4, byteorder=sys.byteorder)

bruh = bwidth + bheight
print("bruh-fing")
iy = 0
while iy < height:
    ix = 0
    while ix < width:
        hex = get_pixel_hex(ix, iy)
        bruh = bruh + hex.encode('utf-8')
        ix += 1
    iy += 1
    if not iy == height:
        bruh = bruh + "\n".encode('utf-8')
  
print("done")

with open(f + ".bruh", "wb") as bruhfile:
    bruhfile.write(bruh)
