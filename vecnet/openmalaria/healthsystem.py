# -*- coding: utf-8 -*-
#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Helper functions for OpenMalaria Health System
Please refer to https://docs.google.com/document/d/1-R-0s0vELuUJ-xuQabjwe1BhKCLYqC4-DBxvC0Z0oeI/edit for design notes
"""

# Using dictionary instead of list to simplify debugging.
probability_list = {
    # 0: 7.934353e-05, # This number does not make a lot of sense
    #                   If 0% of people are treated, probability should be 0, isn't it?
    0: 0.0,
    1: 0.003655052,
    2: 0.007259242,
    3: 0.01089065,
    4: 0.01454715,
    5: 0.01821375,
    6: 0.02185895,
    7: 0.02545025,
    8: 0.02895516,
    9: 0.03234127,
    10: 0.03558067,
    11: 0.03870637,
    12: 0.04179515,
    13: 0.04492462,
    14: 0.04817231,
    15: 0.05161556,
    16: 0.05531544,
    17: 0.0592686,
    18: 0.06345559,
    19: 0.0678569,
    20: 0.07245236,
    21: 0.07721322,
    22: 0.08210456,
    23: 0.08709143,
    24: 0.09213899,
    25: 0.09721381,
    26: 0.1022998,
    27: 0.1073931,
    28: 0.1124904,
    29: 0.1175883,
    30: 0.1226833,
    31: 0.1277816,
    32: 0.1329135,
    33: 0.1381124,
    34: 0.1434117,
    35: 0.1488444,
    36: 0.1544396,
    37: 0.1601931,
    38: 0.1660799,
    39: 0.1720749,
    40: 0.1781534,
    41: 0.1842907,
    42: 0.1904703,
    43: 0.1966911,
    44: 0.2029544,
    45: 0.209261,
    46: 0.215612,
    47: 0.2220045,
    48: 0.228417,
    49: 0.2348223,
    50: 0.2411937,
    51: 0.2475042,
    52: 0.2537213,
    53: 0.2598108,
    54: 0.2657407,
    55: 0.271538,
    56: 0.2773034,
    57: 0.2831406,
    58: 0.2891962,
    59: 0.2957379,
    60: 0.3030474,
    61: 0.311396,
    62: 0.3209671,
    63: 0.331772,
    64: 0.3437782,
    65: 0.3566707,
    66: 0.3699061,
    67: 0.3828218,
    68: 0.39491,
    69: 0.4061192,
    70: 0.4164699,
    71: 0.4261829,
    72: 0.4355614,
    73: 0.4448962,
    74: 0.4544731,
    75: 0.4645689,
    76: 0.4754909,
    77: 0.4875557,
    78: 0.5010331,
    79: 0.5159051,
    80: 0.5318855,
    81: 0.5483645,
    82: 0.5644357,
    83: 0.5793443,
    84: 0.5929385,
    85: 0.6057272,
    86: 0.6184566,
    87: 0.6318566,
    88: 0.6465634,
    89: 0.6629652,
    90: 0.6812664,
    91: 0.7013116,
    92: 0.7223719,
    93: 0.7436717,
    94: 0.7665125,
    95: 0.7933986,
    96: 0.8262853,
    97: 0.8660768,
    98: 0.9114032,
    99: 0.9580364,
    100: 0.9984184
}


def get_prob_from_percentage(perc):
    """
    Converted percentage of people treated to probability of being treated on a timestep
    """
    assert isinstance(perc, int)
    assert perc < 101
    assert perc >= 0

    return probability_list[perc]


def get_percentage_from_prob(prob):
    """
    Converted probability of being treated to total percentage of clinical cases treated
    """
    assert isinstance(prob, (float, int))
    prob = float(prob)
    assert prob >= 0
    assert prob <= 1

    percentages = probability_list.keys()
    percentages.sort()
    for percentage in percentages:
        if prob < probability_list[percentage]:
            return percentage - 1
    return 100
