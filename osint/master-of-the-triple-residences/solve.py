import hashlib

name = "Henri_De_Toulouse-Lautrec"

hash_name = hashlib.sha256(name.encode())
hex_hash_name = hash_name.hexdigest()

print("ctf{",hex_hash_name,"}")
