from pwn import *

HOST = '34.185.173.244'
PORT = '31825'

def solve():
    conn = remote(HOST,PORT)
    
    conn.recvuntil(b'> ')
    conn.sendline(b'2')

    conn.recvuntil(b'Token > ')

    conn.sendline(b'0' * 64)

    conn.recvline()
    
    #bruteforce 16 bytes
    for i in range(256):
        hex_byte = f"{i:02x}"
        guess_payload = hex_byte * 16

        conn.recvuntil(b'> ')
        conn.sendline(b'1')

        conn.recvuntil(b'Password > ')
        conn.sendline(guess_payload.encode())

        response = conn.recvline().decode().strip()
        if "Wrong password!" not in response:
            print(response)
            break

    conn.close()
    

if __name__ == "__main__":
    solve()