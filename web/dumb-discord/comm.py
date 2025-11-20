def obfuscate(byt):
    mask = b'ctf{tryharderdontstring}'
    lmask = len(mask)
    return bytes((c ^ mask[i % lmask] for i, c in enumerate(byt)))

def test(s):
    data = obfuscate(s.encode())
    return data


print(test('\x00\x00\x00\x00E\x10A\x0e\x00E\x02VA\x00\x0eXC\x17\x12\x17\x0b_\x03H\x05C_CAB\x1d\x0b\x07CWSAT\r[AEG\x17PVRKU\x16\x00L\x16EOZYC\x00QB]\x0bYFK\x17D\x14').decode())
