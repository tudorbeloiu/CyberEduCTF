from pwn import *
import base64
import re
import ast


def xor(first, second):
    length = max(len(second), len(first))
    data = b''
    i, j = 0, 0
    for _ in range(length):
        data += (first[i] ^ second[j]).to_bytes(1, 'big')
        i += 1
        j += 1
        i %= len(first)
        j %= len(second)
        if i == 0 or j == 0:
            return data
    return data

HOST = "34.89.183.202"
PORT = 32109

conn = remote(HOST,PORT)
myData = b"A"*39

print(conn.recvline())
prompt = conn.recvuntil(b"Your data >")
print(prompt)

conn.sendline(myData)

enc_string = conn.recvline()
print(enc_string)

s = enc_string.decode(errors="ignore")
m = re.search(r'(b([\'"]).*?\2)', s, flags=re.DOTALL)


token = m.group(1)
parsed = ast.literal_eval(token)


print(b"parsed len =", len(parsed))
print(b"parsed hex =", parsed.hex())

xored = parsed[-len(myData):]
secret = parsed[:len(myData)]
key_part = xor(xored, myData)
flag_part = xor(secret, key_part)

print(flag_part)
print(key_part)


conn.close()