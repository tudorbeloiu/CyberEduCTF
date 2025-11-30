from scapy.all import *
from scapy.layers.http import *

packets = rdpcap("radio.pcapng")

urls = []

for pkt in packets:
    if pkt.haslayer(HTTPRequest):
        if pkt[HTTPRequest].Method == b"GET":
            host = pkt[HTTPRequest].Host.decode()
            path = pkt[HTTPRequest].Path.decode()

            if "/image/" in path:
                full_url = f"http://{host}{path}"
                if full_url not in urls:
                    urls.append(full_url)

with open("image_urls.txt", "w") as g:
    for url in urls:
        g.write(url + "\n")

