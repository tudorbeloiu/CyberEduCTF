import requests
import base64

token = "WeXhJc1clzUvezwtR7xcEgKC6nDLnY6AtN8bOqvi"

alphabet = [chr(x) for x in range(97,123)]
numbers = [x for x in range(1,99)]

for n in numbers:
    url = "http://34.185.175.147:31371/router.php?token=" + token + "&cmd="
    cmd_b64 = base64.b64encode(str(n).encode()).decode()
    url = url + cmd_b64
    r = requests.get(url)
    if "String not allowed." not in r.text:
        print(n)