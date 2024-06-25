from cryptography.fernet import Fernet

key = "aI1VNWqKJaT6XWmT5yWFMo5oNWqc2D4lUyEGX9bVFMA="

systemInfo = "systemInfoEnc.txt"
clipInfo = "clipboardEnc.txt"
keyLogInfo = "keyLogEnc.txt"

encFiles = [systemInfo, clipInfo, keyLogInfo]
count = 0

for decryptingFiles in encFiles:
    with open(decryptingFiles[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open(encFiles[count], 'wb') as f:
        f.write(decrypted)
    count += 1