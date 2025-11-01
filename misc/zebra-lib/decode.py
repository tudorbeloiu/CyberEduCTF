from pwn import *
import base64
import zlib
import re

HOST = "34.159.84.4"
PORT = 31779

def decode_message(encoded_message):

    decoded_bytes = base64.urlsafe_b64decode(encoded_message)
    dec_bytes = zlib.decompress(decoded_bytes)

    return dec_bytes


conn = remote(HOST,PORT)

while True:
    print(conn.recvline())
    encoded_message = conn.recvline().decode('utf-8').replace("\r\n","")
    print(encoded_message)
    decoded_message = decode_message(encoded_message)
    print(decoded_message)
    conn.sendline((decoded_message))
    print(conn.recvline())

conn.close()