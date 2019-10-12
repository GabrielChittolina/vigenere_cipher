import collections
import numpy as np

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
    return r

def load_words():
    with open('english_words_1000', 'r') as wordsf:
        aux = set(wordsf.read().split())
    return aux

def ultra_decipher(ct):
    data = []
    for i in range(1, 256):
        data.append(decipher(i, ct))

    english_words = load_words()
    res = [0] * 256
    for i, sen in enumerate(data):
        for _, word in enumerate(english_words):
            if word in sen:
                res[i] += len(word)

    return data[res.index(max(res))]


def guess_key(ct):
    r = [0] * len(ct)
    for i, _ in enumerate(ct):
        for j in range(i + 1, len(ct)):
            if ct[i] == ct[j]:
                r[j - i - 1] += 1
    rr = []
    avg = np.mean(r[:int(len(r)/10)])

    return r


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
    print(principal_period(find_key(d, data)))
    
    guess_key(cipher(key, tt))

    # print(d)
    # print(ultra_decipher(d))

if __name__ == "__main__":
    main()
