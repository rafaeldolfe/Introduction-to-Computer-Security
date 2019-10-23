import random

def xorIntArrays(data, key): 
    if (len(data) != len(key)):
        raise Exception('The given integer lists are not of equal length')
    barray = []
    for a, b in zip(data, key):
        d = a ^ b
        barray.append(d)
    return barray

def randomIntArray(length):
    tmp = []
    for i in range(length):
        tmp.append(random.getrandbits(8))
    return tmp

def getBMPLength(img):
    imgb = open(img, 'rb').read()
    return len(imgb[54:])

def cipher(img, out, key):
    imgb = open(img, 'rb').read()
    header = imgb[0:54]
    body = imgb[54:]

    img = [x for x in body] # make into int array

    cipher = bytes(xorIntArrays(img, key))

    newFile = open(out, 'wb')
    newFile.write(header + cipher)

def oneTimeCipherBMP(img, out):
    imgKey = randomIntArray(getBMPLength(img))
    cipher(img, out, imgKey)
    return imgKey

def twoTimeCipherBMPs(img1, img2, out1, out2):
    imgKey = randomIntArray(getBMPLength(img1))
    cipher(img1, out1, imgKey)
    cipher(img2, out2, imgKey)
    return imgKey

def stringToIntArray(strlist):
    tmp = []
    for char in strlist:
        tmp.append(ord(char))
    return tmp
def intArrayToHexString(intarray):
    decode = ''
    for item in intarray:
        hexed = hex(item)[2:]
        if (len(hex(item)[2:]) == 1):
            hexed = hexed + '0'
        decode = decode + hexed
    return decode

#### Task 1 ####
#### Convert the strings in to integer arrays, then use the xorIntArray, then finally hex the numbers ####

darlin = 'Darlin dont you go'
andcut = 'and cut your hair!'

darlin_array = stringToIntArray(darlin)
andcut_array = stringToIntArray(andcut)

xored = xorIntArrays(darlin_array, andcut_array)

hexstring = intArrayToHexString(xored)

print(hexstring)

#### Task 2 and 3 ####
mustang = 'mustang.bmp'
logo = 'cp-logo.bmp'

#### Open mustang.bmp, read it into a byte array, generate a key equally long, and encrypt it using XOR ####
mustangCipher = 'mustang-cipher.bmp'
mustangKey = oneTimeCipherBMP(mustang, mustangCipher)


#### Open cp-logo.bmp, read it into a byte array, generate a key equally long, and encrypt it using XOR ####
logoCipher = 'logo-cipher.bmp'
logoKey = oneTimeCipherBMP(logo, logoCipher)

#### decrypt into a regular image again by reading the cipher and XOR:ing it with the remembered key for that cipher ####
cipher('mustang-cipher.bmp', 'back-to-mustang1.bmp', mustangKey)
cipher('logo-cipher.bmp', 'back-to-logo1.bmp', logoKey)

#### Task 4 ####
#### Open mustang.bmp and cp-logo.bmp, generate a key, encrypt both with that key ####
twoTimeCipherBMPs(mustang, logo, 'mustang-encrypted.bmp', 'logo-encrypted.bmp')

#### now XOR the encrypted files ####
mustangEnc = open('mustang-encrypted.bmp', 'rb').read()
header = mustangEnc[0:54]
mustangBody = [x for x in mustangEnc[54:]]

cipher('logo-encrypted.bmp', 'mustangXlogo.bmp', mustangBody)