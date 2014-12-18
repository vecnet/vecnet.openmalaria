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

import math


def is_prime(n):
    """
    Check if n is a prime number
    """
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


def prime_numbers(start_with=2):
    """
    Sequence (generator) of prime numbers starting with start_with number.
    That's it, if start_with is 1000, first number generated will be 1009
    Not the fastest algorithm, but doesn't require a lot of memory
    """
    i = start_with
    while True:
        if is_prime(i):
            yield i
        i += 1
