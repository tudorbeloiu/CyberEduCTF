import requests
import string

l = [ch for ch in string.printable]
url = "http://34.185.173.244:32343/"

param = "name_input"


for ch in l:
    r = requests.get(url, params={param: ch})
    if "Banned characters" in r.text:
        print(ch)

