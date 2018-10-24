# -*- coding: utf-8 -*-

# Copyright 2014-2018 by Christopher C. Little.
# This file is part of Abydos.
#
# Abydos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Abydos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Abydos. If not, see <http://www.gnu.org/licenses/>.

"""abydos.phonetic.caverphone.

The phonetic.caverphone module implements the Caverphone phonetic algorithm.
"""

from __future__ import unicode_literals

__all__ = ['caverphone']


def caverphone(word, version=2):
    """Return the Caverphone code for a word.

    A description of version 1 of the algorithm can be found in
    :cite:`Hood:2002`.

    A description of version 2 of the algorithm can be found in
    :cite:`Hood:2004`.

    :param str word: the word to transform
    :param int version: the version of Caverphone to employ for encoding
        (defaults to 2)
    :returns: the Caverphone value
    :rtype: str

    >>> caverphone('Christopher')
    'KRSTFA1111'
    >>> caverphone('Niall')
    'NA11111111'
    >>> caverphone('Smith')
    'SMT1111111'
    >>> caverphone('Schmidt')
    'SKMT111111'

    >>> caverphone('Christopher', 1)
    'KRSTF1'
    >>> caverphone('Niall', 1)
    'N11111'
    >>> caverphone('Smith', 1)
    'SMT111'
    >>> caverphone('Schmidt', 1)
    'SKMT11'
    """
    _vowels = {'a', 'e', 'i', 'o', 'u'}

    word = word.lower()
    word = ''.join(c for c in word if c in
                   {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                    'y', 'z'})

    def _squeeze_replace(word, char):
        """Convert strings of char in word to one instance of new_char."""
        while char * 2 in word:
            word = word.replace(char * 2, char)
        return word.replace(char, char.upper())

    # the main replacement algorithm
    if version != 1 and word[-1:] == 'e':
        word = word[:-1]
    if word:
        if word[:5] == 'cough':
            word = 'cou2f'+word[5:]
        if word[:5] == 'rough':
            word = 'rou2f'+word[5:]
        if word[:5] == 'tough':
            word = 'tou2f'+word[5:]
        if word[:6] == 'enough':
            word = 'enou2f'+word[6:]
        if version != 1 and word[:6] == 'trough':
            word = 'trou2f'+word[6:]
        if word[:2] == 'gn':
            word = '2n'+word[2:]
        if word[-2:] == 'mb':
            word = word[:-1]+'2'
        for src, tar in (('cq', '2q'), ('ci', 'si'), ('ce', 'se'),
                         ('cy', 'sy'), ('tch', '2ch'), ('c', 'k'), ('q', 'k'),
                         ('x', 'k'), ('v', 'f'), ('dg', '2g'), ('tio', 'sio'),
                         ('tia', 'sia'), ('d', 't'), ('ph', 'fh'), ('b', 'p'),
                         ('sh', 's2'), ('z', 's')):
            word = word.replace(src, tar)
        if word[0] in _vowels:
            word = 'A'+word[1:]
        for vowel in 'aeiou':
            word = word.replace(vowel, '3')
        if version != 1:
            word = word.replace('j', 'y')
            if word[:2] == 'y3':
                word = 'Y3'+word[2:]
            if word[:1] == 'y':
                word = 'A'+word[1:]
            word = word.replace('y', '3')
        for src, tar in (('3gh3', '3kh3'), ('gh', '22'), ('g', 'k')):
            word = word.replace(src, tar)

        for char in 'stpkfmn':
            word = _squeeze_replace(word, char)

        word = word.replace('w3', 'W3')
        if version == 1:
            word = word.replace('wy', 'Wy')
        word = word.replace('wh3', 'Wh3')
        if version == 1:
            word = word.replace('why', 'Why')
        if version != 1 and word[-1:] == 'w':
            word = word[:-1]+'3'
        word = word.replace('w', '2')
        if word[:1] == 'h':
            word = 'A'+word[1:]
        word = word.replace('h', '2')
        word = word.replace('r3', 'R3')
        if version == 1:
            word = word.replace('ry', 'Ry')
        if version != 1 and word[-1:] == 'r':
            word = word[:-1]+'3'
        word = word.replace('r', '2')
        word = word.replace('l3', 'L3')
        if version == 1:
            word = word.replace('ly', 'Ly')
        if version != 1 and word[-1:] == 'l':
            word = word[:-1]+'3'
        word = word.replace('l', '2')
        if version == 1:
            word = word.replace('j', 'y')
            word = word.replace('y3', 'Y3')
            word = word.replace('y', '2')
        word = word.replace('2', '')
        if version != 1 and word[-1:] == '3':
            word = word[:-1]+'A'
        word = word.replace('3', '')

    # pad with 1s, then extract the necessary length of code
    word += '1'*10
    if version != 1:
        word = word[:10]
    else:
        word = word[:6]

    return word


if __name__ == '__main__':
    import doctest
    doctest.testmod()