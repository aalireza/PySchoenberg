"""
This file is part of PySchoenberg.

    PySchoenberg is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, Version 2.

    PySchoenberg is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PySchoenberg.  If not, see <http://www.gnu.org/licenses/>.
"""


from Crypto.Cipher import AES
from getpass import getpass
import MusicToolbox
import binascii

BLOCKSIZE = 16
PADDING_CHAR = '\x00'
# This particular implementation uses only keys that are in range(24)
NUM_REPO = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g',
            17: 'h', 18: 'i', 19: 'j', 20: 'k', 21: 'l', 22: 'm', 23: 'n',
            24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't', 30: 'u',
            31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z', 36: '~', 37: '!',
            38: '@', 39: '#', 40: '$', 41: '%', 42: '^', 43: '&', 44: '*',
            45: '?', 46: '>', 47: '_'}
NUM_REPO_COMPLIMENT = {i: str(i) for i in range(10)}
NUM_REPO_COMPLETE = dict(NUM_REPO_COMPLIMENT.items() + NUM_REPO.items())


def base10toN(number, n):
    """
    Parameters
    ----------
    number:         int
                    A number in base 10
    n:              int
                    The target base

    Returns
    -------
    newNumString:   str
                    `number` in base `n` using NUM_REPO to represent digits
    """
    # Code from http://code.activestate.com/recipes/65212
    newNumString = ''
    current = number
    while current != 0:
        remainder = current % n
        if 48 > remainder > 9:
            remainderString = NUM_REPO[remainder]
        elif remainder >= 36:
            remainderString = '(' + str(remainder) + ')'
        else:
            remainderString = str(remainder)
        newNumString = remainderString + newNumString
        current = current/n
    return newNumString


def baseNto10(number, base):
    """
    Parameters
    ----------
    number:     str
                A number is base `base`
    base:       int
                The current base

    Returns
    -------
    result:     int
                `number` in base 10
    """
    result = 0
    number = list(str(number))
    number.reverse()
    for i in range(len(number)):
        for j in NUM_REPO_COMPLETE:
            if number[i] == NUM_REPO_COMPLETE[j]:
                result += int(j) * base ** int(i)
    return result


def pad(x):
    """
    Pads `x` to divide BLOCKSIZE

    Parameters
    ----------
    x:          str

    Returns
    -------
    padded:     str
    """
    topad = BLOCKSIZE - (len(x) % BLOCKSIZE)
    padded = x + topad * PADDING_CHAR
    return padded


def unpad(x):
    """
    Removes PADDING_CHAR from x

    Parameters
    ----------
    x:          str

    Returns
    -------
    y:          str
    """
    y = x.rstrip(PADDING_CHAR)
    return y


def encrypt(text, key):
    """
    Encrypts AES-128 and returns the result in base 24

    Parameters
    ----------
    text:               str
                        Plain text
    key:                str
                        Encryption key

    Returns
    -------
    finalCiphertext:    str
                        Cipher text in base 24

    See Also
    --------
    padding(x), decrypt(ciphertext, key), AES.AESCipher(...)
    """
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    if len(text) % BLOCKSIZE != 0:
        text = pad(text)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(text)
    b16 = binascii.hexlify(bytearray(ciphertext))
    finalCiphertext = base10toN(baseNto10(b16, 16), 24)
    return finalCiphertext


def decrypt(ciphertext, key):
    """
    Decrypts AES-128 encrypted ciphertext and returns the plain text.

    Parameters
    ----------
    ciphertext:         str
                        Should be in base 24
    key:                str
                        Encryption key

    Returns
    -------
    plainText:          str

    See Also
    ---------
    pad(x), encrypt(text, key), AES.AESCipher(...)
    """
    if len(key) % BLOCKSIZE != 0:
        key = pad(key)
    ciphertext16 = base10toN(baseNto10(ciphertext, 24), 16)
    ct = binascii.unhexlify(ciphertext16)
    cipher = AES.AESCipher(key, AES.MODE_ECB)
    plainText = unpad(cipher.decrypt(ct))
    return plainText


def getEncryptionKey():
    """
    Returns
    -------
    key:        str
                Key used for encryption.
    """
    key = None
    confirmationKey = False
    while confirmationKey != key:
        key = getpass("What is your encryption key? ")
        confirmationKey = getpass("Repeat your key: ")
        if key != confirmationKey:
            print "Your key doesn't match its confirmation"
    return key


def ciphernum(ciphertext):
    """
    Gets a ciphertext and produces the number of each character based on
    NUM_REPO_COMPLETE. Since The ciphertext will be in base 24, it'll be used to
    map a row/column on a 12 tone later.

    Parameters
    ----------
    ciphertext:         str

    Returns
    -------
    listCharNum:        [int]
                        An ordered list of numbers. Each number maps a
                        character of the ciphertext
    """
    cipherlist = list(ciphertext)
    cipherlist.reverse()
    listCharNum = []
    initialCipherlistLength = len(cipherlist)
    for i in range(initialCipherlistLength):
        temp = cipherlist.pop()
        for j in range(len(NUM_REPO_COMPLETE.keys())):
            if temp == NUM_REPO_COMPLETE[j]:
                listCharNum.append(j)
                break
    return listCharNum


def stackProducer(ciphertextNumbers, rowColumnNumbers, fileXml):
    """
    The way that this program encodes a ciphertext in base 24, is to map each
    character of the ciphetext to a row/column of the 12 tone matrix, then
    getting that row/column and mapping every number on it to a note and filling
    fileXml. This function produces a stack of enough numbers from row/columns
    to fill the fileXml

    Parameters
    ----------
    ciphertextNumbers:      [int]
                            An ordered list of numbers. Each number maps a
                            character of the ciphertext
    rowColumnNumbers:       {int: [int]}
                            A dictionary of methods, connecting range(24) to
                            rows and columns of a 12-tone matrix. Number 0 to 11
                            are for rows and then 12 to 23 are for columns.
    fileXml:                str
                            Absolute path of the MusicXML file.

    Returns
    -------
    Bool                    False
                            If the number of needed notes to put every character
                            of the ciphertext inside a musical sheet is more
                            than the number of notes inside that sheet. It'll
                            return False, since this program doesn't change the
                            rhythm and deals with pitch classes which is not
                            enough (i.e. no duration)when we run out of notes.
    stack:                  [[int]]
                            A list whose elements are rows/columns of a 12 tone
                            matrix i.e. stack contains lists of list of ints.

    See Also
    --------
    MusicToolbox.rowColumnNumbers(noteListWithNumbers)
    """
    stack = []
    for element in ciphertextNumbers:
        stack += rowColumnNumbers[element]
    stack.reverse()
    if len(stack) > MusicToolbox.numberOfNotes(fileXml):
        underNotesCount = (len(stack) - MusicToolbox.numberOfNotes(fileXml))
        print ("You lack {} number of notes in your".format(underNotesCount) +
               "sheet. Process is aborted. Please use a larger one.")
        return False
    return stack


def encodingChecker(fileXml):
    """
    Checks whether the probability of of the the fileXml being an encoded file
    is 0 or not by counting the number of its note and to see whether they are
    divisible by 12 (Not particularly accurate way to guess so, but works well
    enough!)

    Parameters
    ----------
    fileXml:        str
                    Absolute path of the fileXml

    Returns
    -------
    Bool            True
                    If the number of notes inside `fileXml` is divisible by 12.
                    False
                    If not True
    """
    if MusicToolbox.numberOfNotes(fileXml) % 12 != 0:
        print "Invalid Encoding: Number of notes not multiple of 12."
        return False
    return True
