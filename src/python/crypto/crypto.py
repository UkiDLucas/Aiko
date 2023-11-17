
# Cell 1

# %% 
print("ciphertext")

# Symmetric-key Encryption
# - encoded and decoded with the same key
# - Anyone with the key can read the data

# %%

## Uncomment lines below to run once
#!conda create -y -n env_ciphertext python=3.11 pip cryptography
print("environment location: ~/.conda/envs/env_ciphertext ")
print("CONTROL-COMMAND-P (⇧⌘P) Select Interpreter  (you might need to press refresh icon)")
print("top right >> SELECT ENVIRONMENTS >> Python EnVIRONMENTS")

#!conda install -y gensim
#!conda install -y -c conda-forge pattern
#!conda install -y pip
#!pip install --upgrade ..


# %%

import base64

data = "my secret needs to be very long"

# Standard Base64 Encoding
encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

print(encodedStr)


import base64

data = "my secret needs to be very long"

# URL and Filename Safe Base64 Encoding
urlSafeEncodedBytes = base64.urlsafe_b64encode(data.encode("utf-8"))
encodedStr = str(urlSafeEncodedBytes, "utf-8")

print(encodedStr)




# %%
from cryptography.fernet import Fernet
 
# we will be encrypting the below string.
message = "hello geeks"
 
# generate a key for encryption and decryption
# You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key

key = Fernet.generate_key()
print("generated key: ", key)
# generated key:  b'SWAVCOjd0JYjxG_fgxSFpzKuF9E8LbLxLtYTkNd845w='
# generated key:  b'FVdpM9V-RSnsYqnOiepK5scfiZ5fU3pYWKYN5oqOQnc='
# generated key:  b'bXkgc2VjcmV0IG5lZWRzIHRvIGJlIHZlcnkgbG9uZw=='

# Instance the Fernet class with the key
 
fernet = Fernet(encodedStr)
 # %%
# then use the Fernet class instance
# to encrypt the string string must
# be encoded to byte string before encryption
encMessage = fernet.encrypt(message.encode())
 
print("original string: ", message)
print("encrypted string: ", encMessage)
 
# decrypt the encrypted string with the
# Fernet instance of the key,
# that was used for encrypting the string
# encoded byte string is returned by decrypt method,
# so decode it to string with decode methods
decMessage = fernet.decrypt(encMessage).decode()
 
print("decrypted string: ", decMessage)

# %%
 

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# %%

def generate_key(master, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt.encode(),
        iterations=100,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master.encode()))
    return key

# %%
def encrypt_text(text, salt):
    key = generate_key(text, salt)
    print("key: ", key)
    encryptor = Fernet(key)
    hash = encryptor.encrypt(text.encode())
    #return hash.decode(), str(key)[2:-1]
    return hash.decode(),  key.decode('utf-8')


def decrypt_text(hash, key_text):
    key = bytes(saved_text, 'utf-8')
    decryptor = Fernet(key)
    text = decryptor.decrypt(hash.encode())
    return text.decode()
# %%
result = encrypt_text("my secret message", "a")
encrypted = result[0]
saved_key = result[1]
print("encrypted: ", encrypted)
print("saved_key: ", saved_key)
# %%
saved_text = "I41_sE8EtPvzb8-XooyiuG4KF_-AuGBDYQNvryTP0BY="
decrypted = decrypt_text(encrypted, saved_text)
print("decrypted: ", decrypted)
# %%
