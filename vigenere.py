from statistics import mode
import numpy as np
import copy

def caesar_decipher(key, data):
    r = ''
    for _, j in enumerate(data):
        r += chr((ord(j) - int(key)) % 256)
    return r

def cipher(key, data):
    r = ''
    for i, j in enumerate(data):
        r += chr((ord(j) + ord(key[i % len(key)])) % 256)
    return r

def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return principal_period(s[:-1]) if i == -1 else s[:i]

def decipher(key, data):
    r = ''
    for i, j in enumerate(data):
        r += chr((ord(j) - ord(key[i % len(key)])) % 256)
    return r

def find_key(ct, t):
    r = ''
    for i in range(len(t)):
        r += chr(ord(ct[i]) - ord(t[i]))
    return principal_period(r)

def load_words():
    with open('english_words_10000', 'r') as wordsf:
        aux = set(wordsf.read().split())
    return aux

def ultra_decipher(ct, key_l=4):
    english_words = load_words()
    ctt = [''] * key_l
    for i in range(len(ct)):
        ctt[i % key_l] += ct[i]

    count = [[0] * 256 for _ in range(key_l)]
    for i, e in enumerate(ctt):
        for j in e:
            count[i][ord(j)] += 1

    for i, e in enumerate(ctt):
        for j, _ in enumerate(count[i]):
            count[i][j] = count[i][j] / len(e)

    freq = [0] * 256
    for _, word in enumerate(english_words):
        for l in word:
            freq[ord(l)] += 1
    freq[ord(' ')] = len(english_words)

    freq_t = 0
    for i in freq:
        freq_t += i

    for i, _ in enumerate(freq):
        freq[i] = freq[i] / freq_t

    f_key = ''
    for i in range(key_l):
        r = []
        for _ in range(len(freq)):
            r.append(np.dot(count[i], freq))
            freq.append(freq.pop(0))
        f_key += chr(r.index(max(r)))
        print(r.index(max(r)))
    print(f_key)
    return decipher(f_key, ct)

def guess_key_len(ct):
    r = [0] * len(ct)
    for i, _ in enumerate(ct):
        for j in range(i + 1, len(ct)):
            if ct[i] == ct[j]:
                r[j - i - 1] += 1

    avg = np.mean(r[:int(len(r)/15)])
    rr = []
    for i, e in enumerate(r):
        if e > avg:
            rr.append(i)

    for i, e in enumerate(r):
        if e > avg:
            rr.append(i)
    rrr = []
    for i in range(1, len(rr)):
        rrr.append(rr[i] - rr[i-1])
    return mode(rrr)


def main():
    with open('in1', 'rb') as inf:
        aux = inf.readlines()
        key = aux[0].decode().strip()
        data = aux[1].decode().strip()

    with open('out1', 'wb') as outf:
        outf.write(cipher(key, data).encode())

    with open('out1', 'rb') as inf:
        d = inf.read().decode().strip()

    with open('text_sample', 'rb') as text:
        tt = text.readlines()
        tt = tt[0].decode().strip()

    print(cipher(key, data))
    print(decipher(key, cipher(key, data)))
    print(find_key(d, data))
    
    # kl = guess_key_len(cipher(key, tt))

    with open('out2', 'wb') as outf:
        outf.write(ultra_decipher(cipher(key, tt), 4).encode())

if __name__ == "__main__":
    main()
