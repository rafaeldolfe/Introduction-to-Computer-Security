from Crypto.Cipher import AES
from OpenSSL import SSL
import matplotlib.pyplot as plt
import random
import time
import datetime


def random16bytes():
    randomInts = []
    for i in range(16):
        randomInts.append(random.randint(0,255))
    return bytes(randomInts)

key = random16bytes()
iv = random16bytes()


def randomnbytes(n):
    randomInts = []
    for i in range(n):
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

def powersof2(n):
    myList = []
    for j in range(1, n+1):
        number = 2 ** j
        myList.append(number)
    return myList

CBCtimes = {}
# 0, 3, 2, 8, 13, 21, 50, 111, 213

blocksizes = []

# for i in powersof2(16):
#     blocksizes.append(1024 * i)

print(blocksizes)

# for blocksize in blocksizes:
#     block = randomnbytes(blocksize)
#     start = datetime.datetime.now()
#     CBC(block)
#     end = datetime.datetime.now()
#     CBCtimes[blocksize] = int((end - start).total_seconds() * 1000)
#     print(int((end - start).total_seconds() * 1000))
# print(CBCtimes)

ECBtimes = {}

# for blocksize in blocksizes:
#     block = randomnbytes(blocksize)
#     start = datetime.datetime.now()
#     ECB(block)
#     end = datetime.datetime.now()
#     ECBtimes[blocksize] = int((end - start).total_seconds() * 1000)
#     print(int((end - start).total_seconds() * 1000))
# print(ECBtimes)

AES128 = {}
AES192 = {}
AES256 = {}

AES128[16] = 24127296
AES128[64] = 6945824
AES128[256] = 1750305
AES128[1024] = 445478
AES128[8192] = 56474
AES128[16384] = 27892

AES192[16] = 20590947
AES192[64] = 5848925
AES192[256] = 1496389
AES192[1024] = 374899
AES192[8192] = 47057
AES192[16384] = 23535

AES256[16] = 18478850
AES256[64] = 4941002
AES256[256] = 1277918
AES256[1024] = 319810
AES256[8192] = 39652
AES256[16384] = 18196

RSAprivate = {}
RSApublic = {}

RSAprivate[512] = 88553
RSAprivate[1024] = 48030
RSAprivate[2048] = 6176
RSAprivate[3072] = 2154
RSAprivate[4096] = 904
RSAprivate[7680] = 107
RSAprivate[15360] = 22
RSApublic[512] = 1199063
RSApublic[1024] = 598018
RSApublic[2048] = 205689
RSApublic[3072] = 99991
RSApublic[4096] = 60493
RSApublic[7680] = 18169
RSApublic[15360] = 4790

# The 'numbers' are in 1000s of bytes per second processed.
# type             16 bytes     64 bytes    256 bytes   1024 bytes   8192 bytes  16384 bytes
# aes-128 cbc     130033.43k   150529.60k   159316.65k   152056.49k   154211.67k   153125.04k
# aes-192 cbc     111561.53k   124130.55k   127691.86k   127965.53k   128496.98k   128532.48k
# aes-256 cbc      98553.87k   105959.92k   109049.00k   109161.81k   108276.39k    99894.71k



lists1 = sorted(AES128.items()) # sorted by key, return a list of tuples
lists2 = sorted(AES192.items()) # sorted by key, return a list of tuples
lists3 = sorted(AES256.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
x3, y3 = zip(*lists3) # unpack a list of pairs into two tuples

print(lists1)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,10))
ax1.title.set_text('Operations / block sizes with aes-128 in 3s')
ax2.title.set_text('Operations / block sizes with aes-192 in 3s')
ax3.title.set_text('Operations / block sizes with aes-256 in 3s')
ax1.plot(x1, y1)
ax2.plot(x2, y2)
ax3.plot(x3, y3)

plt.savefig('openssl.png')
plt.savefig('openssl.png', bbox_inches='tight')


lists1 = sorted(RSAprivate.items()) # sorted by key, return a list of tuples
lists2 = sorted(RSApublic.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
ax1.title.set_text('Operations / bit sizes with rsa private in 10s')
ax2.title.set_text('Operations / bit sizes with rsa public in 10s')
ax1.plot(x1, y1)
ax2.plot(x2, y2)

plt.savefig('openssl-rsa.png')
plt.savefig('openssl-rsa.png', bbox_inches='tight')

