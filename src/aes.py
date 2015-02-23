import binascii
from Crypto.Cipher import AES

blocksize = 16
padchar = '\x00'
num_rep = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g',
           17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n',
           24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't', 30: 'u',
           31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z', 36: '~', 37: '!',
           38: '@', 39: '#', 40: '$', 41: '%', 42: '^', 43: '&', 44: '*',
           45: '?', 46: '>', 47: '_'}
num_rep_compliment = {i: str(i) for i in range(10)}
num_rep_complete = dict(num_rep_compliment.items() + num_rep.items())


def base10toN(num, n):
    # Code from http://code.activestate.com/recipes/65212
    new_num_string = ''
    current = num
    while current != 0:
        remainder = current % n
        if 48 > remainder > 9:
            remainder_string = num_rep[remainder]
        elif remainder >= 36:
            remainder_string = '(' + str(remainder) + ')'
        else:
            remainder_string = str(remainder)
        new_num_string = remainder_string + new_num_string
        current = current/n
    return new_num_string


def baseNto10(num, base):
    result = 0
    num = list(str(num))
    num.reverse()
    for i in range(len(num)):
        for j in num_rep_complete:
            if num[i] == num_rep_complete[j]:
                result += int(j) * base ** int(i)
    return result


def pad(x):
    topad = blocksize - (len(x) % blocksize)
    padded = x + topad * padchar
    return padded


def unpad(x):
    return x.rstrip('\x00')


def encrypt(im, key):
    if len(key) % blocksize != 0:
        key = pad(key)
    if len(im) % blocksize != 0:
        im = pad(im)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(im)
    b16 = binascii.hexlify(bytearray(ciphertext))
    return base10toN(baseNto10(b16, 16), 24)


def decrypt(ciphertext, key):
    if len(key) % blocksize != 0:
        key = pad(key)
    ciphertext16 = base10toN(baseNto10(ciphertext, 24), 16)
    ct = binascii.unhexlify(ciphertext16)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ct))
