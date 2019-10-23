import fileinput

alphabet = "abcdefghijklmnopqrstuvwxyz"

letter_counter = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0,                      "f" : 0,  "g" : 0,
    "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
    "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
    "x" : 0,  "y" : 0,  "z" : 0 }

frequency_analysis = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0,                      "f" : 0,  "g" : 0,
    "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
    "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
    "x" : 0,  "y" : 0,  "z" : 0 }

closeness_analysis = { "a" : 0,  "b" : 0,  "c" : 0,  "d" : 0,  "e" : 0,                      "f" : 0,  "g" : 0,
    "h" : 0,  "i" : 0,  "j" : 0,  "k" : 0,  "l" : 0,  "m" : 0,  "n" : 0,  "o" :   0,
    "p" : 0,  "q" : 0,  "r" : 0,  "s" : 0,  "t" : 0,  "u" : 0,  "v" : 0,  "w" : 0,
    "x" : 0,  "y" : 0,  "z" : 0 }

standard_letter_frequency = { "a" : 0.0812,  "b" : 0.0149,  "c" : 0.0271,  "d" : 0.0432,  "e" : 0.12, "f" : 0.0230,  "g" : 0.0203,
    "h" : 0.0592,  "i" : 0.0731,  "j" : 0.0010,  "k" : 0.0069,  "l" : 0.0398,  "m" : 0.0261,  "n" : 0.0695,  "o" : 0.0768,
    "p" : 0.0182,  "q" : 0.0011,  "r" : 0.0602,  "s" : 0.0628,  "t" : 0.0910,  "u" : 0.0288,  "v" : 0.0111,  "w" : 0.0209,
    "x" : 0.0017,  "y" : 0.0211,  "z" : 0.0007 }

    
everything = ''
counter = 0
for line in fileinput.input():
    everything = everything + line

for char in everything:
    if (char.isalpha()):
        letter_counter[char.lower()] = letter_counter[char.lower()] + 1
        counter = counter + 1

for letter in alphabet:
    frequency_analysis[letter] = letter_counter[letter]/counter

# Do chi square testh ere
for anyletter in alphabet:
    letter = anyletter.lower()
    minimum = 1000000
    list_of_closeness = [letter,{}]
    for standard_letter in alphabet:
        closeness = pow((frequency_analysis[letter] - standard_letter_frequency[standard_letter]), 2)/standard_letter_frequency[standard_letter]
        list_of_closeness[1][standard_letter] = closeness
    list_of_closeness[1] = sorted(list_of_closeness[1].keys(),key=lambda item: list_of_closeness[1][item])

    closeness_analysis[letter] = list_of_closeness[1]

print(frequency_analysis)
print(closeness_analysis)

monoMap = {}

print("sorted(frequency_analysis.keys(),key=lambda item: frequency_analysis[item], reverse=True)")
print(sorted(frequency_analysis.keys(),key=lambda item: frequency_analysis[item], reverse=True))
used_letters = []

letters_to_guess = sorted(frequency_analysis.keys(),key=lambda item: frequency_analysis[item], reverse=True)
for already_guessed in monoMap.keys():
    letters_to_guess.remove(already_guessed)

for already_used in monoMap.values():
    used_letters.append(already_used)

for letter in letters_to_guess:

    for alternative in closeness_analysis[letter]:
        if (alternative not in used_letters):
            monoMap[letter] = alternative
            used_letters.append(alternative)
            break


guess = ''
for anyletter in everything:
    if (anyletter.isalpha()):
        letter = anyletter.lower()
        if (anyletter.isupper()):
            guess = guess + monoMap[letter].upper()
        else:
            guess = guess + monoMap[letter]
    else: 
        guess = guess + anyletter



print('------------ Decrypted ------------')
print(guess)
print('------------ Cipher text ------------')
print(everything)

c = 0
for letter in sorted(monoMap.keys()):
    if (not c % 4):
        print()
    print(letter + ':' + monoMap[letter] + ' ', end='')
    c = c + 1