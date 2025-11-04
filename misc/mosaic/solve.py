from PIL import Image
import numpy as np
import glob

files = sorted(glob.glob("*.png"))
imgs = [np.array(Image.open(f).convert("RGB")) for f in files]

imgs_stack = np.stack(imgs)

all_white = np.all(imgs_stack == 255, axis=(0, -1))

result = np.zeros_like(imgs[0], dtype=np.uint8)
result[all_white] = [255, 255, 255]

Image.fromarray(result).save("flag_bww.png")

