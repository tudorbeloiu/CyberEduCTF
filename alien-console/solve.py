from pwn import *

context.log_level = "critical"
# stop showing "Connecting to.."/"Closed connection"



def tryFlag(flag):

    expectedZeros = '0' * 2 * len(flag)

    r = remote('34.185.184.46',31296)
    r.recvuntil(b": ")
    r.sendline(flag.encode())
    r.recvuntil((flag + "\r\n").encode()) #skip my input
    resp = r.recvuntil(b"\r\n")[:-2].decode()
    r.close()
    if resp.startswith(expectedZeros):
        return True
    else:
        return False
    
characters = "0123456789abcdef}" #sha256 flg format
flag = "ctf{"

while flag[:-1] != "}":
    for c in characters:
        if tryFlag(flag+c):
            flag = flag + c
            print(flag)
            break
