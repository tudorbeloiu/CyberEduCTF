import base64

encoded_text = "dHNkdktTAVUHAABUA1VWVgIHBAlSBAFTBAMFUwECAgcAAAFWAFUFCFMACFFUAwQAVgBSBwQJBVZTAFYGCQYHVQABB1IJTQ=="
key = 0x30

flag = ""

decoded64_text = base64.b64decode(encoded_text).hex()

for i in range(0, len(decoded64_text), 2):
    hex_x = int(decoded64_text[i:i+2],16)
    flag = flag + chr(hex_x ^ key)

print(flag)