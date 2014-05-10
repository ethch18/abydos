# -*- coding: utf-8 -*-

from itertools import groupby
from string import maketrans
import re


def russell_index(word):
    """Given a string 'word', returns its Int value according to Robert C.
    Russell's Index algorithm, as described in US Patent 1,261,167 (1917)
    """
    word = word.lower()
    word = word.replace('gh', '')  # discard gh (rule 3)
    while word[len(word)-1] in 'sz':
        word = word[:len(word)-2] # discard /[sz]$/ (rule 3)

    """
    abcdefghijklmnopqrstuvwxyz
    12341230103567123834120313
    """

    sdx = ''
    for char in word:
        if char in 'aeiouy' and '1' not in sdx: # rule 1: "oral resonants"
            sdx += '1'
        elif char in 'bfpv': # rule 2: "labials and labio-dentals"
            sdx += '2'
        elif char in 'cgkqxsz': # rule 3: "gutturals and ...  sibilants"
            sdx += '3'
        elif char in 'dt': # rule 4: "dental-mutes"
            sdx += '4'
        elif char is 'l': # rule 5: "palatal fricative"
            sdx += '5'
        elif char is 'm': # rule 6: "labio-nasal"
            sdx += '6'
        elif char is 'n': # rule 7: "dento or lingua-nasal"
            sdx += '7'
        elif char is 'r': # rule 8: "dental-fricative"
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)
    return int(sdx)


def russell_index_num_to_alpha(num):
    """Given the numeric form of a Russell Index value, returns its
    alphabetic form, as described in US Patent 1,261,167 (1917)
    """
    num = str(num)
    return num.translate(maketrans('12345678', 'abcdlmnr'), '09')


def russell_index_alpha(word):
    """Given a string 'word', returns its alphabetic value according to Robert C.
    Russell's Index algorithm, as described in US Patent 1,261,167 (1917)
    """
    return russell_index_num_to_alpha(russell_index(word))


def knuth_soundex(word):
    """As descibed in Knuth(1998:394)
    """
    sdx = ''
    word = word.lower()
    for char in word:
        if char in 'bfpv': # rule 2a
            sdx += '1'
        elif char in 'cgjkqsxz': # rule 2b
            sdx += '2'
        elif char in 'dt': # rule 2c
            sdx += '3'
        elif char is 'l': # rule 2d
            sdx += '4'
        elif char in 'mn': # rule 2e
            sdx += '5'
        elif char is 'r': # rule 2f
            sdx += '6'

        elif char in 'aeiouy': # rule 1
            sdx += '0'
        elif char in 'hw': # rule 1
            sdx += '9'

        else:
            sdx += char

    sdx = sdx.replace('9', '') # rule 1
    sdx = _delete_consecutive_repeats(sdx) # rule 3

    sdx = word[0] + sdx[1:]
    sdx = sdx.replace('0', '') # rule 1

    sdx += '000' # rule 4

    return sdx[:4]


def creativyst_soundex(word):
    """Incorporates enhancements from http://creativyst.com/Doc/Articles/SoundEx1/SoundEx1.htm#Enhancements
    """
    word = word.lower()
    word = word.replace('dg', 'g')
    word = re.sub(r'(.)gn', r'\1n', word)
    word = word.replace('gn', 'n')
    word = word.replace('kn', 'n')
    word = word.replace('ph', 'f')
    word = re.sub('mp([szt])', 'm\1', word)
    word = word.replace('^ps', 's')
    word = word.replace('^pf', 'f')
    word = word.replace('mb', 'm')
    word = word.replace('tch', 'ch')
    word = re.sub('^[ai]([aeio])', 'e', word)

    return knuth_soundex(word)


def koelner_phonetik(word):
    """Given a string 'word', returns its Int value according to the
    Kölner Phonetik
    """
    def _before(word, i, letters):
        if i > 0 and word[i-1] in letters:
            return True
        return False

    def _after(word, i, letters):
        if i+1 < len(word) and word[i+1] in letters:
            return True
        return False

    word = word.lower()
    sdx = ''

    word = word.replace('ä', 'ae')
    word = word.replace('ö', 'oe')
    word = word.replace('ü', 'ue')
    word = word.replace('ß', 'ss')

    for i in range(len(word)):
        if word[i] in 'aeijyou':
            sdx += '0'
        elif word[i] in 'b':
            sdx += '1'
        elif word[i] in 'p':
            if _before(word, i, 'h'):
                sdx += '3'
            else:
                sdx += '1'
        elif word[i] in 'dt':
            if _before(word, i, 'csz'):
                sdx += '8'
            else:
                sdx += '2'
        elif word[i] in 'fvw':
            sdx += '3'
        elif word[i] in 'gkq':
            sdx += '4'
        elif word[i] in 'c':
            if _after(word, i, 'sz'):
                sdx += '8'
            elif i == 0:
                if _after(word, i, 'ahkloqrux'):
                    sdx += '4'
                else:
                    sdx += '8'
            elif _before(word, i, 'ahkoqux'):
                sdx += '4'
            else:
                sdx += '8'
        elif word[i] in 'x':
            if _after(word, i, 'ckq'):
                sdx += '8'
            else:
                sdx += '48'
        elif word[i] in 'l':
            sdx += '5'
        elif word[i] in 'mn':
            sdx += '6'
        elif word[i] in 'r':
            sdx += '7'
        elif word[i] in 'sz':
            sdx += '8'

    sdx = _delete_consecutive_repeats(sdx)

    sdx = sdx.replace('0', '')

    return int(sdx)


def koelner_phonetik_num_to_alpha(num):
    """Given the numeric form of a Kölner Phonetik value, returns an
    alphabetic form
    """
    num = str(num)
    return num.translate(maketrans('012345678', 'aptfklnrs'))


def koelner_phonetik_alpha(word):
    """Given a string 'word', returns an alphabetic value representing
    its Kölner Phonetik value
    """
    return koelner_phonetik_num_to_alpha(koelner_phonetik(word))


def nysiis(word):
    return word


def mra(word):
    return word


def metaphone(word):
    return word


def double_metaphone(word):
    return word


def caverphone(word, version=2):
    word = word.lower()
    word = filter(lambda c: c in 'abcdefghijklmnopqrstuvwxyz', word)

    if version!=1 and word.endswith('e'):
        word = word[:-1]
    if word.startswith('cough'):
        word = 'cou2f'+word[5:]
    if word.startswith('rough'):
        word = 'rou2f'+word[5:]
    if word.startswith('tough'):
        word = 'tou2f'+word[5:]
    if word.startswith('enough'):
        word = 'enou2f'+word[6:]
    if version!=1 and word.startswith('trough'):
        word = 'trou2f'+word[6:]
    if word.startswith('gn'):
        word = '2n'+word[2:]
    if word.endswith('mb'):
        word = word[:-1]+'2'
    word = word.replace('cq', '2q')
    word = word.replace('ci', 'si')
    word = word.replace('ce', 'se')
    word = word.replace('cy', 'sy')
    word = word.replace('tch', '2ch')
    word = word.replace('c', 'k')
    word = word.replace('q', 'k')
    word = word.replace('x', 'k')
    word = word.replace('v', 'f')
    word = word.replace('dg', '2g')
    word = word.replace('tio', 'sio')
    word = word.replace('tia', 'sia')
    word = word.replace('d', 't')
    word = word.replace('ph', 'fh')
    word = word.replace('b', 'p')
    word = word.replace('sh', 's2')
    word = word.replace('z', 's')
    if word[0] in 'aeiou':
        word = 'A'+word[1:]
    word = word.replace('a', '3')
    word = word.replace('e', '3')
    word = word.replace('i', '3')
    word = word.replace('o', '3')
    word = word.replace('u', '3')
    if version!=1:
        word = word.replace('j', 'y')
        if word.startswith('y3'):
            word = 'Y3'+word[2:]
        if word.startswith('y'):
            word = 'A'+word[1:]
        word = word.replace('y', '3')
    word = word.replace('3gh3', '3kh3')
    word = word.replace('gh', '22')
    word = word.replace('g', 'k')
    word = re.sub(r's+', r'S', word)
    word = re.sub(r't+', r'T', word)
    word = re.sub(r'p+', r'P', word)
    word = re.sub(r'k+', r'K', word)
    word = re.sub(r'f+', r'F', word)
    word = re.sub(r'm+', r'M', word)
    word = re.sub(r'n+', r'N', word)
    word = word.replace('w3', 'W3')
    if version==1:
        word = word.replace('wy', 'Wy')
    word = word.replace('wh3', 'Wh3')
    if version==1:
        word = word.replace('why', 'Why')
    if version!=1 and word.endswith('w'):
        word = word[:-1]+'3'
    word = word.replace('w', '2')
    if word.startswith('h'):
        word = 'A'+word[1:]
    word = word.replace('h', '2')
    word = word.replace('r3', 'R3')
    if version==1:
        word = word.replace('ry', 'Ry')
    if version!=1 and word.endswith('r'):
        word = word[:-1]+'3'
    word = word.replace('r', '2')
    word = word.replace('l3', 'L3')
    if version==1:
        word = word.replace('ly', 'Ly')
    if version!=1 and word.endswith('l'):
        word = word[:-1]+'3'
    word = word.replace('l', '2')
    if version==1:
        word = word.replace('j', 'y')
        word = word.replace('y3', 'Y3')
        word = word.replace('y', '2')
    word = word.replace('2', '')
    if version!=1 and word.endswith('3'):
        word = word[:-1]+'A'
    word = word.replace('3', '')
    word = word+'1'*10
    if version!=1:
        word = word[:10]
    else:
        word = word[:6]  

    return word


"""def phonemicize_graphemes(word):
    phones = word
    #phones = phones.replace(
"""

def _delete_consecutive_repeats(word):
    return ''.join(char for char, _ in groupby(word))
