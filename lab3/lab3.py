from hashlib import sha256
import string
import itertools
import time
from math import ceil
import matplotlib.pyplot as plt

alphabet_extra = "abcdefghijklmnopqrstuvwxyz123456"

def sha256_truncate(bstring, bits_to_output):
    digest = sha256(bstring.encode('utf-8')).digest()
    intarray = [b for b in digest][0:(ceil(bits_to_output/8))]
    last = ceil(bits_to_output/8) - 1
    and_value = 255
    if (bits_to_output % 8 == 2):
        and_value = 3
    elif (bits_to_output % 8 == 4):
        and_value = 15
    elif (bits_to_output % 8 == 6):
        and_value = 63
    
    intarray[last] = intarray[ceil(bits_to_output/8) - 1] & and_value
    sbarray = str(bytearray(intarray))
    return sbarray
    
def binhamming(string1, string2):
    bin1 = ' '.join(map(bin,bytearray(string1,'utf8')))
    bin2 = ' '.join(map(bin,bytearray(string2,'utf8')))
    return hamming(bin1, bin2)

def hamming(string1, string2):
    dist = 0
    len1 = len(string1)
    len2 = len(string2)
    if (len1 > len2):
        dist = len1 - len2
    elif (len2 > len1):
         dist = len2 - len1
    for a, b in zip(list(string1), list(string2)):
        if a is not b:
            dist+=1
    return dist

def find_collision(bitsize):
    stored_hashes = {}
    attempts = 0
    for size in range(1,len(alphabet_extra)):
        perms = itertools.permutations(alphabet_extra[0:size], size)
        for p in perms:
            seq = "".join(p)
            attempts += 1
            curr = sha256_truncate(seq, bitsize)
            if curr in stored_hashes:
                return (attempts, stored_hashes[curr], seq)
            else:
                stored_hashes[curr] = seq

bitsizes = []

for i in range(26):
    if (i < 4):
        continue
    bitsizes.append(i * 2)

print(bitsizes)





#### Task 1b ####

testwords = ['hello', 'monster', 'divide', 'o2', 'sample']
nearbywords = ['hell', 'monste', 'divid', 'o', 'sampl']

close_pairs = []

for i in range(len(testwords)):
    for letter in alphabet_extra:
        if (binhamming(testwords[i], nearbywords[i] + letter) == 1):
            print('word1: ', testwords[i], ' word2: ', nearbywords[i] + letter)
            close_pairs.append((testwords[i], nearbywords[i] + letter))
            break

hash_pairs = []
bin_pairs = []

for close_pair in close_pairs:
    hash_pairs.append((sha256(close_pair[0].encode('utf8')).hexdigest(), sha256(close_pair[1].encode('utf8')).hexdigest()))
    bin_pairs.append((bin(int(sha256(close_pair[0].encode('utf8')).hexdigest(), 16))[2:].zfill(256), bin(int(sha256(close_pair[1].encode('utf8')).hexdigest(), 16))[2:].zfill(256)))

print('length of a sha256 hexdigest: ', len(hash_pairs[0][0]))
for i in range(len(hash_pairs)):
    print('hamming distance for pair ' + str(i) + ':', binhamming(hash_pairs[i][0][0:1],hash_pairs[i][1][0:1]))

print('length of a sha256 hexdigest: ', len(bin_pairs[0][0]))
for i in range(len(bin_pairs)):
    print('hamming distance for pair ' + str(i) + ':', hamming(bin_pairs[i][0],bin_pairs[i][1]))

#### Task 1c ####

number_of_inputs = {}
collision_times = {}
bitsizes = bitsizes
for bitsize in bitsizes:
    start = time.time()
    collision = find_collision(bitsize)
    end = time.time()
    collision_time = end - start
    number_of_inputs[bitsize] = (collision[0])
    collision_times[bitsize] = collision_time
    print('--------------bitsize: ' + str(bitsize) + '--------------- ')
    print("time: ", collision_time, " attempts: ", collision[0], " sequence1: ", collision[1], " sequence2: ", collision[2])

print(collision_times)

lists1 = sorted(collision_times.items()) # sorted by key, return a list of tuples
lists2 = sorted(number_of_inputs.items()) # sorted by key, return a list of tuples

x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.title.set_text('Time / digest size')
ax2.title.set_text('Number of inputs / digest size')
ax1.plot(x1, y1)
ax2.plot(x2, y2)
ax1.set_xticks(bitsizes, minor=False)
ax2.set_xticks(bitsizes, minor=False)

plt.savefig('foo.png')
plt.savefig('foo.pdf')
plt.savefig('bar.png', bbox_inches='tight')



