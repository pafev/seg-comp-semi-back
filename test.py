from hashlib import sha3_256


a = sha3_256("aaaaadadasdasdasdasdasdasaa".encode())
print(a.digest_size)

print(len(a.digest()))
