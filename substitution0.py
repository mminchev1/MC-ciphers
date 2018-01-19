import numpy as np
import string
import random, math

data = open('C:/Users/User/ciphers/data.txt', 'r')
data = data.read()
data = data.lower()

M = np.zeros((26, 26))
count = 0

for i in range(len(data)-1):
    a, b = ord(data[i]), ord(data[i+1])
    if 96 < a < 123 and 96 < b < 123:
        M[a-97][b-97] += 1
        count += 1
        
for i in range(26):
    M[i, :] = M[i, :]/ sum(M[i, :])


m = 'The score function can be basically any function,\
which returns the higher value the more likely the text\
appears to be written in English.'

m1 = 'The algorithm proceeds by randomly attempting to move in the key space\
to more correct state, sometimes accepting the moves and sometimes remaining\
in the state. The randomness allows accepting the less plausible keys and\
prevents from getting stuck in local maximum. Note that the acceptance\
ratio indicates how probable is the new proposed key with respect\
to the current key.'

m2 = 'Instead of men endowed with divine authority and directly guided by\
the will of God, modern history has given us either heroes endowed with\
extraordinary, superhuman capacities, or simply men of very various\
kinds, from monarchs to journalists, who lead the masses. Instead of the\
former divinely appointed aims of the Jewish, Greek, or Roman nations,\
which ancient historians regarded as representing the progress of\
humanity, modern history has postulated its own aims—the welfare of the\
French, German, or English people, or, in its highest abstraction, the\
welfare and civilization of humanity in general, by which is usually\
meant that of the peoples occupying a small northwesterly portion of a\
large continent.'


def score(s):
    value = 0
    for i in range(len(s)-1):
        a, b = ord(s[i]), ord(s[i+1])
        if 96 < a < 123 and 96 < b < 123:
                value += M[a-97][b-97]
    return(-value)


def decrypt(s, key):
    s = s.lower()
    ans = ''
    for i in range(len(s)):
        a = ord(s[i])
        if 96 < a < 123:
            ans += key[ord(s[i])-97]
        else:
            ans += s[i]
    return ans


def break_ceaser(s):
    key = list(string.ascii_lowercase)
#
#    np.random.shuffle(key)
    beta = 1.0
    n_accept = 0
    best_energy = float('inf')
    energy = score(decrypt(s, key))

    for step in range(1000000):
        if n_accept == 100:
            beta *= 1.005
            n_accept = 0
        p = random.uniform(0.0, 1.0)

        if p < 1:
            new_key = key.copy()
            i = random.randint(0, 25)
            j = random.choice(list(range(i)) + list(range(i+1, 26)))
            new_key[i], new_key[j] = new_key[j], new_key[i]

        new_energy = score(decrypt(s, new_key))

        if random.uniform(0.0, 1.0) < math.exp(- beta * (new_energy - energy)):
            n_accept += 1
            energy = new_energy
            key = new_key
            if energy < best_energy:
                
                best_energy = energy
                best_key = key.copy()
                print(best_energy, step)
                print(decrypt(s, best_key))
#        if step % 100000 == 0:
#        print energy, step, 1.0 / beta
    print(decrypt(s, best_key))

#break_ceaser(m)           
