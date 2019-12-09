from Crypto.Cipher import AES
import random

def random16bytes():
    randomInts = []
    for i in range(16):
        randomInts.append(random.randint(0,255))
    return bytes(randomInts)

def ECB(plaintext):
    key = random16bytes()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def CBC(plaintext):
    key = random16bytes()
    iv = random16bytes()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def PKCS7(byteArray):
    paddingLength = (128 - len(byteArray) % 128) % 128
    for i in range(paddingLength):
        byteArray.append(paddingLength)
    return byteArray

img ='mustang.bmp'
outimgECB ='ECB.bmp'
outimgCBC ='CBC.bmp'

imgb = open(img, 'rb').read()
header = imgb[0:54]
body = imgb[54:]
bytearrayBody = bytearray(body)

bytearrayBody = PKCS7(bytearrayBody)

cipherbody = ECB(bytearrayBody)


cipher = bytes(cipherbody)

newFile = open(outimgECB, 'wb')
newFile.write(header + cipher)

cipherbody = CBC(bytearrayBody)


cipher = bytes(cipherbody)

newFile = open(outimgCBC, 'wb')
newFile.write(header + cipher)