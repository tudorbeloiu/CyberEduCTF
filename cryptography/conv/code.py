def conv(array1:bytes, array2:bytes) -> bytes:
    len1, len2 = len(array1), len(array2)
    res = [0]*(len1 + len2 - 1)
    for i in range(len1 + len2 - 1):
        csum = 0
        for j in range(max(0, i - len2 + 1), min(len1, i + 1)):
            csum += array1[j] * array2[i - j]
        res[i] = csum % 256
    return res

key = b'\xab\xec\xe9<\xaaC\x7fr\xeb\x8dgQ\xc0\x94\x01\x1d\xc03\x14\x97\xe2\x91\x97\xcf\x8b\x13?\x1d24w|'
cip = conv(plain1,key)
print(bytes(cip).hex())