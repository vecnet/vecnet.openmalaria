#!/bin/env python2
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

import sys

from vecnet.openmalaria.experiment_creator_v2 import ExperimentDescription

def main(*args):
    if len(args) != 2:
        print "USAGE: %s filename" % sys.argv[0]
        return -1
        # filename = "experiment1.json"
        # exit(0)
    else:
        filename = sys.argv[1]

    print filename
    with open(filename) as fp:
        exp = ExperimentDescription(fp)

    i = 1
    for scenario in exp.scenarios():
        with open("scenario%s.xml" % i, "w") as fp:
            fp.write(scenario)
        i += 1
    print "%s scenarios generated" % (i-1)
    return 0

if __name__ == "__main__":
    status = main(*sys.argv)
    sys.exit(status)
