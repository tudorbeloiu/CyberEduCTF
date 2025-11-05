import base64
from Crypto.Cipher import ChaCha20

data = {"nonce": "kjvH0GtuxGQ=", "ciphertext": "QEHqAOAQXzoEhxCKvJElCR0N+qjFhEFtKdZfE8VYyYqy8tonzAMrL7xfksV3yhhlP3pgwLUSIDwEEWGpCajvFPiT/EuF", 
        "key": "Fidel_Alejandro_Castro_Ruz_Cuba!"}

nonce = base64.b64decode(data['nonce'])
ciphertext = base64.b64decode(data['ciphertext'])
key = data['key'].encode('utf-8')

cipher = ChaCha20.new(key=key,nonce=nonce)
flag = cipher.decrypt(ciphertext)
print(flag)
try:
    print(flag.decode('utf-8'))
except UnicodeDecodeError:
    print("Kaput engine")
