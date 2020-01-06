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

"""abydos.tests.tokenizer.test_tokenizer_q_skipgrams.

This module contains unit tests for abydos.tokenizer.QGrams
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import unittest
from collections import Counter

from abydos.tokenizer import QSkipgrams


class QSkipgramsTestCases(unittest.TestCase):
    """Test abydos.tokenizer.QSkipgrams."""

    def test_qskipgrams(self):
        """Test abydos.tokenizer.QSkipgrams."""
        self.assertEqual(sorted(QSkipgrams().tokenize('').get_list()), [])
        self.assertEqual(
            sorted(QSkipgrams(start_stop='').tokenize('a').get_list()), []
        )
        self.assertEqual(
            sorted(QSkipgrams().tokenize('a').get_list()), ['$#', '$a', 'a#']
        )
        self.assertEqual(
            sorted(QSkipgrams().tokenize('ab').get_list()),
            sorted(['$a', '$b', '$#', 'ab', 'a#', 'b#']),
        )

        self.assertEqual(
            sorted(QSkipgrams().tokenize('NELSON').get_list()),
            sorted(
                [
                    '$N',
                    '$E',
                    '$L',
                    '$S',
                    '$O',
                    '$N',
                    '$#',
                    'NE',
                    'NL',
                    'NS',
                    'NO',
                    'NN',
                    'N#',
                    'EL',
                    'ES',
                    'EO',
                    'EN',
                    'E#',
                    'LS',
                    'LO',
                    'LN',
                    'L#',
                    'SO',
                    'SN',
                    'S#',
                    'ON',
                    'O#',
                    'N#',
                ]
            ),
        )
        self.assertEqual(
            sorted(QSkipgrams().tokenize('NEILSEN').get_list()),
            sorted(
                [
                    '$N',
                    '$E',
                    '$I',
                    '$L',
                    '$S',
                    '$E',
                    '$N',
                    '$#',
                    'NE',
                    'NI',
                    'NL',
                    'NS',
                    'NE',
                    'NN',
                    'N#',
                    'EI',
                    'EL',
                    'ES',
                    'EE',
                    'EN',
                    'E#',
                    'IL',
                    'IS',
                    'IE',
                    'IN',
                    'I#',
                    'LS',
                    'LE',
                    'LN',
                    'L#',
                    'SE',
                    'SN',
                    'S#',
                    'EN',
                    'E#',
                    'N#',
                ]
            ),
        )

        self.assertEqual(
            sorted(QSkipgrams(qval=1).tokenize('NEILSEN').get_list()),
            sorted(['N', 'E', 'I', 'L', 'S', 'E', 'N']),
        )

        test_counter = (
            QSkipgrams(qval=(2,), scaler='SSK')
            .tokenize('NEILSEN')
            .get_counter()
        )
        gold_counter = Counter(
            {
                '$N': 1.2404672100000003,
                '$E': 1.2072969000000002,
                '$I': 0.6561,
                '$L': 0.5904900000000001,
                '$S': 0.531441,
                '$#': 0.3874204890000001,
                'NE': 1.341441,
                'NI': 0.7290000000000001,
                'NL': 0.6561,
                'NS': 0.5904900000000001,
                'NN': 0.4782969000000001,
                'N#': 1.2404672100000003,
                'EI': 0.81,
                'EL': 0.7290000000000001,
                'ES': 0.6561,
                'EE': 0.5904900000000001,
                'EN': 1.341441,
                'E#': 1.2072969000000002,
                'IL': 0.81,
                'IS': 0.7290000000000001,
                'IE': 0.6561,
                'IN': 0.5904900000000001,
                'I#': 0.531441,
                'LS': 0.81,
                'LE': 0.7290000000000001,
                'LN': 0.6561,
                'L#': 0.5904900000000001,
                'SE': 0.81,
                'SN': 0.7290000000000001,
                'S#': 0.6561,
            }
        )
        for key in gold_counter.keys():
            self.assertAlmostEqual(gold_counter[key], test_counter[key])

        test_counter = (
            QSkipgrams(qval=(4, 6, 5, 1, 0), scaler='SSK')
            .tokenize('NIALL')
            .get_counter()
        )
        gold_counter = Counter(
            {
                '$$$N': 0.531441,
                '$$$I': 0.4782969000000001,
                '$$$A': 0.4304672100000001,
                '$$$L': 0.7360989291000002,
                '$$$#': 0.8504267154039002,
                '$$NI': 1.4880348000000003,
                '$$NA': 1.3392313200000003,
                '$$NL': 2.2900855572000007,
                '$$N#': 2.645772003478801,
                '$$IA': 1.3392313200000003,
                '$$IL': 2.2900855572000007,
                '$$I#': 2.645772003478801,
                '$$AL': 2.2900855572000007,
                '$$A#': 2.645772003478801,
                '$$LL': 1.0847773692000002,
                '$$L#': 5.291544006957601,
                '$$##': 2.460275073345601,
                '$NIA': 1.4402051100000002,
                '$NIL': 2.462750738100001,
                '$NI#': 2.845254813264901,
                '$NAL': 2.462750738100001,
                '$NA#': 2.845254813264901,
                '$NLL': 1.1665661391000004,
                '$NL#': 5.690509626529802,
                '$N##': 2.645772003478801,
                '$IAL': 2.462750738100001,
                '$IA#': 2.845254813264901,
                '$ILL': 1.1665661391000004,
                '$IL#': 5.690509626529802,
                '$I##': 2.645772003478801,
                '$ALL': 1.1665661391000004,
                '$AL#': 5.690509626529802,
                '$A##': 2.645772003478801,
                '$LL#': 2.845254813264901,
                '$L##': 5.291544006957601,
                '$###': 0.8504267154039002,
                'NIAL': 1.0097379000000002,
                'NIA#': 1.1665661391000002,
                'NILL': 0.4782969000000001,
                'NIL#': 2.3331322782000004,
                'NI##': 1.0847773692000002,
                'NALL': 0.4782969000000001,
                'NAL#': 2.3331322782000004,
                'NA##': 1.0847773692000002,
                'NLL#': 1.1665661391000002,
                'NL##': 2.1695547384000005,
                'N###': 0.3486784401000001,
                'IALL': 0.531441,
                'IAL#': 2.5923691980000005,
                'IA##': 1.2053081880000003,
                'ILL#': 1.2961845990000003,
                'IL##': 2.4106163760000006,
                'I###': 0.3874204890000001,
                'ALL#': 1.4402051100000004,
                'AL##': 2.6784626400000007,
                'A###': 0.4304672100000001,
                'LL##': 1.4880348000000003,
                'L###': 1.0097379000000002,
                '$$$$$N': 0.3486784401000001,
                '$$$$$I': 0.31381059609000006,
                '$$$$$A': 0.2824295364810001,
                '$$$$$L': 0.48295450738251017,
                '$$$$$#': 0.8431447750407974,
                '$$$$NI': 1.6039208244600003,
                '$$$$NA': 1.4435287420140006,
                '$$$$NL': 2.468434148843941,
                '$$$$N#': 4.309406627986299,
                '$$$$IA': 1.4435287420140006,
                '$$$$IL': 2.468434148843941,
                '$$$$I#': 4.309406627986299,
                '$$$$AL': 2.468434148843941,
                '$$$$A#': 4.309406627986299,
                '$$$$LL': 1.1692582810313406,
                '$$$$L#': 8.618813255972597,
                '$$$$##': 7.715070145397851,
                '$$$NIA': 2.984687447256001,
                '$$$NIL': 5.103815534807762,
                '$$$NI#': 8.910270709073119,
                '$$$NAL': 5.103815534807762,
                '$$$NA#': 8.910270709073119,
                '$$$NLL': 2.417596832277361,
                '$$$NL#': 17.82054141814625,
                '$$$N##': 15.951932474542438,
                '$$$IAL': 5.103815534807762,
                '$$$IA#': 8.910270709073119,
                '$$$ILL': 2.417596832277361,
                '$$$IL#': 17.82054141814625,
                '$$$I##': 15.951932474542438,
                '$$$ALL': 2.417596832277361,
                '$$$AL#': 17.82054141814625,
                '$$$A##': 15.951932474542438,
                '$$$LL#': 8.910270709073119,
                '$$$L##': 31.903864949084834,
                '$$$###': 15.08638445665049,
                '$$NIAL': 5.396635688803742,
                '$$NIA#': 9.42147782919388,
                '$$NILL': 2.556301115749141,
                '$$NIL#': 18.84295565838777,
                '$$NI##': 16.867139400002937,
                '$$NALL': 2.556301115749141,
                '$$NAL#': 18.84295565838777,
                '$$NA##': 16.867139400002937,
                '$$NLL#': 9.42147782919388,
                '$$NL##': 33.73427880000585,
                '$$N###': 15.951932474542435,
                '$$IALL': 2.556301115749141,
                '$$IAL#': 18.84295565838777,
                '$$IA##': 16.867139400002937,
                '$$ILL#': 9.42147782919388,
                '$$IL##': 33.73427880000585,
                '$$I###': 15.951932474542435,
                '$$ALL#': 9.42147782919388,
                '$$AL##': 33.73427880000585,
                '$$A###': 15.951932474542435,
                '$$LL##': 16.867139400002937,
                '$$L###': 31.903864949084824,
                '$$####': 7.715070145397851,
                '$NIALL': 1.4278730800535104,
                '$NIAL#': 10.525109490228838,
                '$NIA##': 9.421477829193876,
                '$NILL#': 5.262554745114417,
                '$NIL##': 18.842955658387766,
                '$NI###': 8.910270709073117,
                '$NALL#': 5.262554745114417,
                '$NAL##': 18.842955658387766,
                '$NA###': 8.910270709073117,
                '$NLL##': 9.421477829193876,
                '$NL###': 17.820541418146256,
                '$N####': 4.309406627986299,
                '$IALL#': 5.262554745114417,
                '$IAL##': 18.842955658387766,
                '$IA###': 8.910270709073117,
                '$ILL##': 9.421477829193876,
                '$IL###': 17.820541418146256,
                '$I####': 4.309406627986299,
                '$ALL##': 9.421477829193876,
                '$AL###': 17.820541418146256,
                '$A####': 4.309406627986299,
                '$LL###': 8.910270709073117,
                '$L####': 8.618813255972595,
                '$#####': 0.8431447750407974,
                'NIALL#': 1.4278730800535104,
                'NIAL##': 5.112602231498281,
                'NIA###': 2.417596832277361,
                'NILL##': 2.556301115749141,
                'NIL###': 4.835193664554721,
                'NI####': 1.1692582810313406,
                'NALL##': 2.556301115749141,
                'NAL###': 4.835193664554721,
                'NA####': 1.1692582810313406,
                'NLL###': 2.417596832277361,
                'NL####': 2.338516562062681,
                'N#####': 0.2287679245496101,
                'IALL##': 2.8403345730546006,
                'IAL###': 5.3724374050608015,
                'IA####': 1.2991758678126004,
                'ILL###': 2.6862187025304003,
                'IL####': 2.5983517356252004,
                'I#####': 0.2541865828329001,
                'ALL###': 2.984687447256001,
                'AL####': 2.887057484028001,
                'A#####': 0.2824295364810001,
                'LL####': 1.6039208244600003,
                'L#####': 0.6624890361900002,
                '$$$$N': 0.4304672100000001,
                '$$$$I': 0.3874204890000001,
                '$$$$A': 0.3486784401000001,
                '$$$$L': 0.5962401325710002,
                '$$$$#': 0.8741476583623434,
                '$$$NI': 1.5927286770000002,
                '$$$NA': 1.4334558093000005,
                '$$$NL': 2.4512094339030006,
                '$$$N#': 3.59371815104519,
                '$$$IA': 1.4334558093000005,
                '$$$IL': 2.4512094339030006,
                '$$$I#': 3.59371815104519,
                '$$$AL': 2.4512094339030006,
                '$$$A#': 3.59371815104519,
                '$$$LL': 1.1610992055330005,
                '$$$L#': 7.187436302090378,
                '$$$##': 4.91876456439945,
                '$$NIA': 2.2513435083000006,
                '$$NIL': 3.849797399193001,
                '$$NI#': 5.644187966956859,
                '$$NAL': 3.849797399193001,
                '$$NA#': 5.644187966956859,
                '$$NLL': 1.8235882417230007,
                '$$NL#': 11.28837593391372,
                '$$N##': 7.725266868411147,
                '$$IAL': 3.849797399193001,
                '$$IA#': 5.644187966956859,
                '$$ILL': 1.8235882417230007,
                '$$IL#': 11.28837593391372,
                '$$I##': 7.725266868411147,
                '$$ALL': 1.8235882417230007,
                '$$AL#': 11.28837593391372,
                '$$A##': 7.725266868411147,
                '$$LL#': 5.644187966956859,
                '$$L##': 15.4505337368223,
                '$$###': 4.918764564399449,
                '$NIAL': 2.812715796861001,
                '$NIA#': 4.123722629777913,
                '$NILL': 1.3323390616710005,
                '$NIL#': 8.247445259555828,
                '$NI##': 5.644187966956858,
                '$NALL': 1.3323390616710005,
                '$NAL#': 8.247445259555828,
                '$NA##': 5.644187966956858,
                '$NLL#': 4.123722629777913,
                '$NL##': 11.288375933913724,
                '$N###': 3.593718151045189,
                '$IALL': 1.3323390616710005,
                '$IAL#': 8.247445259555828,
                '$IA##': 5.644187966956858,
                '$ILL#': 4.123722629777913,
                '$IL##': 11.288375933913724,
                '$I###': 3.593718151045189,
                '$ALL#': 4.123722629777913,
                '$AL##': 11.288375933913724,
                '$A###': 3.593718151045189,
                '$LL##': 5.644187966956858,
                '$L###': 7.187436302090377,
                '$####': 0.8741476583623434,
                'NIALL': 0.4304672100000001,
                'NIAL#': 2.664678123342001,
                'NIA##': 1.8235882417230007,
                'NILL#': 1.3323390616710005,
                'NIL##': 3.6471764834460014,
                'NI###': 1.1610992055330005,
                'NALL#': 1.3323390616710005,
                'NAL##': 3.6471764834460014,
                'NA###': 1.1610992055330005,
                'NLL##': 1.8235882417230007,
                'NL###': 2.322198411066001,
                'N####': 0.2824295364810001,
                'IALL#': 1.4803767351900001,
                'IAL##': 4.0524183149400015,
                'IA###': 1.2901102283700003,
                'ILL##': 2.0262091574700007,
                'IL###': 2.5802204567400007,
                'I####': 0.31381059609000006,
                'ALL##': 2.2513435083000006,
                'AL###': 2.8669116186000005,
                'A####': 0.3486784401000001,
                'LL###': 1.5927286770000004,
                'L####': 0.8178876990000001,
                'N': 1.0,
                'I': 1.0,
                'A': 1.0,
                'L': 2.0,
            }
        )
        for key in gold_counter.keys():
            self.assertAlmostEqual(gold_counter[key], test_counter[key])

        self.assertEqual(
            QSkipgrams(qval=(2, 3), scaler='length')
            .tokenize('NIALL')
            .get_counter(),
            Counter(
                {
                    '$N': 2,
                    '$I': 2,
                    '$A': 2,
                    '$L': 4,
                    '$#': 2,
                    'NI': 2,
                    'NA': 2,
                    'NL': 4,
                    'N#': 2,
                    'IA': 2,
                    'IL': 4,
                    'I#': 2,
                    'AL': 4,
                    'A#': 2,
                    'LL': 2,
                    'L#': 4,
                    '$$N': 3,
                    '$$I': 3,
                    '$$A': 3,
                    '$$L': 6,
                    '$$#': 6,
                    '$NI': 6,
                    '$NA': 6,
                    '$NL': 12,
                    '$N#': 12,
                    '$IA': 6,
                    '$IL': 12,
                    '$I#': 12,
                    '$AL': 12,
                    '$A#': 12,
                    '$LL': 6,
                    '$L#': 24,
                    '$##': 6,
                    'NIA': 3,
                    'NIL': 6,
                    'NI#': 6,
                    'NAL': 6,
                    'NA#': 6,
                    'NLL': 3,
                    'NL#': 12,
                    'N##': 3,
                    'IAL': 6,
                    'IA#': 6,
                    'ILL': 3,
                    'IL#': 12,
                    'I##': 3,
                    'ALL': 3,
                    'AL#': 12,
                    'A##': 3,
                    'LL#': 6,
                    'L##': 6,
                }
            ),
        )
        test_counter = (
            QSkipgrams(qval=(2, 3), scaler='length-log')
            .tokenize('NIALL')
            .get_counter()
        )
        gold_counter = Counter(
            {
                '$N': 1.0986122886681096,
                '$I': 1.0986122886681096,
                '$A': 1.0986122886681096,
                '$L': 2.197224577336219,
                '$#': 1.0986122886681096,
                'NI': 1.0986122886681096,
                'NA': 1.0986122886681096,
                'NL': 2.197224577336219,
                'N#': 1.0986122886681096,
                'IA': 1.0986122886681096,
                'IL': 2.197224577336219,
                'I#': 1.0986122886681096,
                'AL': 2.197224577336219,
                'A#': 1.0986122886681096,
                'LL': 1.0986122886681096,
                'L#': 2.197224577336219,
                '$$N': 1.3862943611198906,
                '$$I': 1.3862943611198906,
                '$$A': 1.3862943611198906,
                '$$L': 2.772588722239781,
                '$$#': 2.772588722239781,
                '$NI': 2.772588722239781,
                '$NA': 2.772588722239781,
                '$NL': 5.545177444479562,
                '$N#': 5.545177444479562,
                '$IA': 2.772588722239781,
                '$IL': 5.545177444479562,
                '$I#': 5.545177444479562,
                '$AL': 5.545177444479562,
                '$A#': 5.545177444479562,
                '$LL': 2.772588722239781,
                '$L#': 11.090354888959125,
                '$##': 2.772588722239781,
                'NIA': 1.3862943611198906,
                'NIL': 2.772588722239781,
                'NI#': 2.772588722239781,
                'NAL': 2.772588722239781,
                'NA#': 2.772588722239781,
                'NLL': 1.3862943611198906,
                'NL#': 5.545177444479562,
                'N##': 1.3862943611198906,
                'IAL': 2.772588722239781,
                'IA#': 2.772588722239781,
                'ILL': 1.3862943611198906,
                'IL#': 5.545177444479562,
                'I##': 1.3862943611198906,
                'ALL': 1.3862943611198906,
                'AL#': 5.545177444479562,
                'A##': 1.3862943611198906,
                'LL#': 2.772588722239781,
                'L##': 2.772588722239781,
            }
        )
        for key in gold_counter.keys():
            self.assertAlmostEqual(gold_counter[key], test_counter[key])

        test_counter = (
            QSkipgrams(qval=(2, 3), scaler='length-exp')
            .tokenize('NIALL')
            .get_counter()
        )
        gold_counter = Counter(
            {
                '$N': 7.38905609893065,
                '$I': 7.38905609893065,
                '$A': 7.38905609893065,
                '$L': 14.7781121978613,
                '$#': 7.38905609893065,
                'NI': 7.38905609893065,
                'NA': 7.38905609893065,
                'NL': 14.7781121978613,
                'N#': 7.38905609893065,
                'IA': 7.38905609893065,
                'IL': 14.7781121978613,
                'I#': 7.38905609893065,
                'AL': 14.7781121978613,
                'A#': 7.38905609893065,
                'LL': 7.38905609893065,
                'L#': 14.7781121978613,
                '$$N': 20.085536923187668,
                '$$I': 20.085536923187668,
                '$$A': 20.085536923187668,
                '$$L': 40.171073846375336,
                '$$#': 40.171073846375336,
                '$NI': 40.171073846375336,
                '$NA': 40.171073846375336,
                '$NL': 80.34214769275067,
                '$N#': 80.34214769275067,
                '$IA': 40.171073846375336,
                '$IL': 80.34214769275067,
                '$I#': 80.34214769275067,
                '$AL': 80.34214769275067,
                '$A#': 80.34214769275067,
                '$LL': 40.171073846375336,
                '$L#': 160.68429538550137,
                '$##': 40.171073846375336,
                'NIA': 20.085536923187668,
                'NIL': 40.171073846375336,
                'NI#': 40.171073846375336,
                'NAL': 40.171073846375336,
                'NA#': 40.171073846375336,
                'NLL': 20.085536923187668,
                'NL#': 80.34214769275067,
                'N##': 20.085536923187668,
                'IAL': 40.171073846375336,
                'IA#': 40.171073846375336,
                'ILL': 20.085536923187668,
                'IL#': 80.34214769275067,
                'I##': 20.085536923187668,
                'ALL': 20.085536923187668,
                'AL#': 80.34214769275067,
                'A##': 20.085536923187668,
                'LL#': 40.171073846375336,
                'L##': 40.171073846375336,
            }
        )
        for key in gold_counter.keys():
            self.assertAlmostEqual(gold_counter[key], test_counter[key])


if __name__ == '__main__':
    unittest.main()
