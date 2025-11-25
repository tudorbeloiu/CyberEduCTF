import requests

url = "http://35.242.200.20:32038/backup/"

r = requests.get(url)

with open("arch.zip", "wb") as g:
    g.write(r.content)

