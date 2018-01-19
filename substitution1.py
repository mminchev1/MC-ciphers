import numpy as np
import string
import random, math

data = open('C:/Users/User/ciphers/data.txt', 'r')
data = data.read()
data = data.lower()
data = ''.join(x for x in data if x.isalpha())

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
 
m3 = '''Modern history has rejected the beliefs of the ancients without
replacing them by a new conception, and the logic of the situation has
obliged the historians, after they had apparently rejected the divine
authority of the kings and the “fate” of the ancients, to reach the same
conclusion by another road, that is, to recognize (1) nations guided
by individual men, and (2) the existence of a known aim to which these
nations and humanity at large are tending.

At the basis of the works of all the modern historians from Gibbon to
Buckle, despite their seeming disagreements and the apparent novelty of
their outlooks, lie those two old, unavoidable assumptions.

In the first place the historian describes the activity of individuals
who in his opinion have directed humanity (one historian considers
only monarchs, generals, and ministers as being such men, while another
includes also orators, learned men, reformers, philosophers, and poets).
Secondly, it is assumed that the goal toward which humanity is being led
is known to the historians: to one of them this goal is the greatness of
the Roman, Spanish, or French realm; to another it is liberty, equality,
and a certain kind of civilization of a small corner of the world called
Europe.

In 1789 a ferment arises in Paris; it grows, spreads, and is expressed
by a movement of peoples from west to east. Several times it moves
eastward and collides with a countermovement from the east westward.
In 1812 it reaches its extreme limit, Moscow, and then, with remarkable
symmetry, a countermovement occurs from east to west, attracting to
it, as the first movement had done, the nations of middle Europe. The
counter movement reaches the starting point of the first movement in the
west—Paris—and subsides.

During that twenty-year period an immense number of fields were left
untilled, houses were burned, trade changed its direction, millions
of men migrated, were impoverished, or were enriched, and millions
of Christian men professing the law of love of their fellows slew one
another.

What does all this mean? Why did it happen? What made those people burn
houses and slay their fellow men? What were the causes of these events?
What force made men act so? These are the instinctive, plain, and
most legitimate questions humanity asks itself when it encounters the
monuments and tradition of that period.'''


def score(s):
    value = 0
    s = s.lower()
    s = ''.join(x for x in s if x.isalpha())
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
    np.random.shuffle(key)
    beta = 1.0
    n_accept = 0
    best_energy = float('inf')
    energy = score(decrypt(s, key))

    for step in range(1000000):
        if n_accept == 100:
            beta *= 1.005
            n_accept = 0
        p = random.uniform(0.0, 1.0)

#        if p  < 0.2:
#            i = random.randint(0, 26 / 2)
#            key = key[i:] + key[:i]
#            i = random.randint(0, 26 / 2)
#            a = key[:i]
#            a.reverse()
#            new_key =  a + key[i:]
#        
        if p < 1:
            new_key = key.copy()
            i = random.randint(0, 25)
            j = random.choice(list(range(i)) + list(range(i+1, 26)))
            new_key[i], new_key[j] = new_key[j], new_key[i]
        
        else:
            new_key = key[:]
            i = random.randint(0, 25 )
            a = new_key.pop(i)
            j = random.randint(0, 24)
            new_key.insert(j, a)

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
