from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("encKey.txt", "wb")
file.write(key)
file.close()