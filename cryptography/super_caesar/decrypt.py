
encrypted1 = "bcjac --- YnuNmQPGhQWqCXGUxuXnFVqrUVCUMhQdaHuCIrbDIcUqnKxbPORYTzVCDBlmAqtKnEJcpED --- UVQR"
w1,w2,w3 = encrypted1.split(" --- ")

s = ""

for e1 in range(0,26):
    for e2 in range(0,26):
        s = ""
        for letter in w2:
            if 65 <= ord(letter) <= 90:
                if ord(letter) - e2 < 65:
                    new_ord = ord(letter) + ((-e2) % 26)
                else:
                    new_ord = ord(letter) - e2

            elif 97 <= ord(letter) <= 122:
                if ord(letter) - e1 < 97:
                    new_ord = ord(letter) + ((-e1) % 26)
                else:
                    new_ord = ord(letter) - e1

            new_letter = chr(new_ord)
            s = s + new_letter
        if 'ECSC' in s.upper() or 'FLAG' in s.upper():
            print(s)

                


