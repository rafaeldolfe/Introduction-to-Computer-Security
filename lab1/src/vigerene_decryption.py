import io
import re
import math


num_to_alphabet = {
    0: "a",
    1: "b",
    2: 'c',
    3: "d",
    4: "e",
    5: 'f',
    6: "g",
    7: "h",
    8: 'i',
    9: "j",
    10: "k",
    11: 'l',
    12: "m",
    13: "n",
    14: 'o',
    15: "p",
    16: "q",
    17: 'r',
    18: "s",
    19: "t",
    20: 'u',
    21: "v",
    22: "w",
    23: 'x',
    24: "y",
    25: "z",
}
alphabet_to_num = {
    "a": 0,
    "b": 1,
    'c': 2,
    "d": 3,
    "e": 4,
    'f': 5,
    "g": 6,
    "h": 7,
    'i': 8,
    "j": 9,
    "k": 10,
    'l': 11,
    "m": 12,
    "n": 13,
    'o': 14,
    "p": 15,
    "q": 16,
    'r': 17,
    "s": 18,
    "t": 19,
    'u': 20,
    "v": 21,
    "w": 22,
    'x': 23,
    "y": 24,
    "z": 25,
}

filename = "ciphers/vigerene_hard_encrypt.txt"
keylength = 13


f = io.open(filename,encoding="utf8")
text = f.read().lower()

alphatext = re.sub(r'[^a-zA-Z]', '', text)

alphabet = "abcdefghijklmnopqrstuvwxyz"
L = []
already_checked_words = []
factor_counter = {}

def shift(text, amount):
    temp = list(text)
    for i in range(len(temp)):
        temp[i] = num_to_alphabet[(alphabet_to_num[temp[i]] + amount) % 26]
    return temp


standard_letter_frequency = { "a" : 0.0812,  "b" : 0.0149,  "c" : 0.0271,  "d" : 0.0432,  "e" : 0.12, "f" : 0.0230,  "g" : 0.0203,
    "h" : 0.0592,  "i" : 0.0731,  "j" : 0.0010,  "k" : 0.0069,  "l" : 0.0398,  "m" : 0.0261,  "n" : 0.0695,  "o" : 0.0768,
    "p" : 0.0182,  "q" : 0.0011,  "r" : 0.0602,  "s" : 0.0628,  "t" : 0.0910,  "u" : 0.0288,  "v" : 0.0111,  "w" : 0.0209,
    "x" : 0.0017,  "y" : 0.0211,  "z" : 0.0007 }

lists_of_closeness = []
lists = []
for i in range(keylength):
    lists.append([])
    lists_of_closeness.append([])

i = 0
index = -1
while (index < len(text) - 1):
    index += 1
    if (not text[index].isalpha()):
        continue
    lists[i % keylength].append(text[index])
    i = i + 1
    
analyses = []
for i in range(len(lists)):
    list_of_closeness = {}
    for amount in range(26):
        counter = 0
        frequency_analysis = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0, "f" : 0,  "g" : 0,
    "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
    "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
    "x" : 0,  "y" : 0,  "z" : 0 }
        letter_counter = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0, "f" : 0,  "g" : 0,
    "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
    "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
    "x" : 0,  "y" : 0,  "z" : 0 }
        shifted = shift(lists[i], amount)
        for letter in shifted:
            if (letter.isalpha()):
                letter_counter[letter.lower()] = letter_counter[letter.lower()] + 1
                counter = counter + 1
        summ = 0
        for letter in alphabet:
            frequency_analysis[letter] = letter_counter[letter]/counter
            closeness = pow((frequency_analysis[letter] - standard_letter_frequency[letter]), 2)/standard_letter_frequency[letter]
            summ = summ + closeness
        
        list_of_closeness[amount] = summ
    lists_of_closeness[i] = sorted(list_of_closeness.keys(),key=lambda item: list_of_closeness[item])

guess = ''

best_shift_amounts = []


for i in range(len(lists)):
    best_shift_amounts.append(lists_of_closeness[i][0])

i = 0
index = -1
while (index < len(text) - 1):
    index += 1
    if (not text[index].isalpha()):
        guess = guess + text[index]
        continue
        
    guess = guess + ''.join(shift(text[index], best_shift_amounts[i % keylength]))
    i = i + 1

print(guess)

for i in range(len(lists)):
    print(num_to_alphabet[lists_of_closeness[i][0]])
    

    