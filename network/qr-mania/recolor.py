from PIL import Image
from pyzbar.pyzbar import decode
from pathlib import Path
import os

in_dir = Path("/home/tudor/ctf/network/qr-mania/pngs")
out_dir = Path("/home/tudor/ctf/network/qr-mania/pngs_bw")

def bw_convert(file_path):
    imag = Image.open(file_path).convert("RGBA")
    pixels = imag.load()

    bg_color = pixels[1,1]
    inside_color = ()

    for x in range(imag.size[0]):
        for y in range(imag.size[1]):
            if pixels[x,y] == bg_color:
                pixels[x,y] = (255,255,255,255)
            else:
                inside_color = pixels[x,y]
                pixels[x,y] = (0,0,0,255)
    destination_path = out_dir / file_path.name
    imag.save(destination_path)
    return destination_path



png_files = list(in_dir.glob("*.png"))

for file_color in png_files:
    out_path = bw_convert(file_color)
    print("saved: ", out_path)