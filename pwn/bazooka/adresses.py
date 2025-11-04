from pwn import *

elf = ELF('./pwn_bazooka_bazooka')
print("puts@got= ", hex(elf.got['puts']))
print("main= ", hex(elf.symbols["main"]))