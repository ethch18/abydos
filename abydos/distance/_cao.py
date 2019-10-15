# -*- coding: utf-8 -*-

# Copyright 2019 by Christopher C. Little.
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

"""abydos.distance._cao.

Cao's CY dissimilarity.
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from math import log10

from ._token_distance import _TokenDistance

__all__ = ['Cao']


class Cao(_TokenDistance):
    r"""Cao's CY dissimilarity.

    Cao dissimilarity :cite:`Cao:1997`

    .. versionadded:: 0.4.1
    """

    def __init__(self, **kwargs):
        """Initialize Cao instance.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments


        .. versionadded:: 0.4.1

        """
        super(Cao, self).__init__(**kwargs)

    def sim(self, src, tar):
        """Return Cao's CY similarity (CYs) of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cao's CY similarity

        Examples
        --------
        >>> cmp = Cao()
        >>> cmp.sim('cat', 'hat')
        0.0
        >>> cmp.sim('Niall', 'Neil')
        0.0
        >>> cmp.sim('aluminum', 'Catalan')
        0.0
        >>> cmp.sim('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()
        in_both_samples = len(self._intersection().items())

        obsereved_cyd = 0
        maximum_cyd = 0
        for symbol in alphabet:
            src_tok = min(0.1, self._src_tokens[symbol])
            tar_tok = min(0.1, self._tar_tokens[symbol])
            tok_sum = src_tok + tar_tok
            obsereved_cyd += (
                tok_sum * log10(tok_sum / 2)
                - src_tok * log10(tar_tok)
                - tar_tok * log10(src_tok)
            ) / tok_sum

            if self._tar_tokens[symbol] == 0:
                maximum_cyd += (
                    (self._src_tokens[symbol] + 0.1)
                    * log10((self._src_tokens[symbol] + 0.1) / 2)
                    - self._src_tokens[symbol] * log10(0.1)
                    - 0.1 * log10(self._src_tokens[symbol])
                ) / (self._src_tokens[symbol] + 0.1)
            elif self._src_tokens[symbol] == 0:
                maximum_cyd += (
                    (self._tar_tokens[symbol] + 0.1)
                    * log10((self._tar_tokens[symbol] + 0.1) / 2)
                    - self._tar_tokens[symbol] * log10(0.1)
                    - 0.1 * log10(self._tar_tokens[symbol])
                ) / (self._tar_tokens[symbol] + 0.1)

        D_i = 0
        D_k = 0
        for symbol in self._intersection().items():
            D_i += self._src_tokens[symbol] - (in_both_samples / 2)
            D_k += self._tar_tokens[symbol] - (in_both_samples / 2)
        D_i /= in_both_samples / 2
        D_k /= in_both_samples / 2

        maximum_cyd += (in_both_samples / 2) * (
            ((D_i + 1) * log10((D_i + 1) / 2) - log10(D_i)) / (D_i + 1)
            + ((D_k + 1) * log10((D_k + 1) / 2) - log10(D_k)) / (D_k + 1)
        )

        return 1 - (obsereved_cyd / maximum_cyd)

    def dist_abs(self, src, tar):
        """Return Cao's CY dissimilarity (CYd) of two strings.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison

        Returns
        -------
        float
            Cao's CY dissimilarity

        Examples
        --------
        >>> cmp = Cao()
        >>> cmp.dist_abs('cat', 'hat')
        0.0
        >>> cmp.dist_abs('Niall', 'Neil')
        0.0
        >>> cmp.dist_abs('aluminum', 'Catalan')
        0.0
        >>> cmp.dist_abs('ATCG', 'TAGC')
        0.0


        .. versionadded:: 0.4.1

        """
        self._tokenize(src, tar)

        alphabet = self._total().keys()

        score = 0
        for symbol in alphabet:
            src_tok = min(0.1, self._src_tokens[symbol])
            tar_tok = min(0.1, self._tar_tokens[symbol])
            tok_sum = src_tok + tar_tok
            score += (
                tok_sum * log10(tok_sum / 2)
                - src_tok * log10(tar_tok)
                - tar_tok * log10(src_tok)
            ) / tok_sum

        return score / sum(self._total().values())


if __name__ == '__main__':
    import doctest

    doctest.testmod()
