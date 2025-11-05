from pathlib import Path
from PIL import Image
from pyzbar.pyzbar import decode
import re

folder = Path("/home/tudor/ctf/network/qr-mania/pngs")
folder_bw = Path("/home/tudor/ctf/network/qr-mania/pngs_bw")

png_files = list(folder.glob("*.png"))
png_file_bw = list(folder_bw.glob("*.png"))

def find_order_number(file_path):
    with open(file_path,"rb") as f:
        data = f.read()

        marker = re.search(rb"(\d{1,2})/69", data)

        number = int(marker.group(1))
        return number

images_in_order = []

for f in png_files:
    order = find_order_number(f)
    images_in_order.append((order,f))

images_in_order.sort(key=lambda x: x[0])

for order_number, file_path in images_in_order:
    print(f"{order_number}/69: {file_path.name}")

flag = ""
for order_number, file_path in images_in_order:
    for file_bw in png_file_bw:
        if file_path.name == file_bw.name:
            dec_obj = decode(Image.open(file_bw))
            flag += dec_obj[0].data.decode("utf-8")
print(flag)


