import hashlib

llave = '4578123547854458'
llave = llave.encode("utf-8")
result = hashlib.md5(llave).hexdigest()

print("The byte equivalent of hash is : ")
print(result)