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
import argparse

from vecnet.openmalaria.experiment import ExperimentSpecification


def main(filename, generate_seed=False):

    with open(filename) as fp:
        exp = ExperimentSpecification(fp)

    i = 1
    keys = exp.experiment["sweeps"].keys()
    csvfile = open("scenarios.csv", "w")
    # Write "header" of csv file
    csvfile.write("filename")
    for key in keys:
        csvfile.write("," + key)
    csvfile.write("\n")

    for scenario in exp.scenarios(generate_seed=generate_seed):
        with open("scenario%s.xml" % i, "w") as fp:
            fp.write(scenario.xml)
        # Write parameters values used to generate this scenario
        csvfile.write("scenario%s.xml" % i)
        for key in keys:
            csvfile.write("," + scenario.parameters.pop(key))
        csvfile.write("\n")
        i += 1
    csvfile.close()
    print "%s scenarios generated" % (i-1)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("exp_spec_name", help="Experiment specification filename")
    parser.add_argument("--seed",
                        help="Automatically replace @seed@ placeholder with a seed number",
                        action="store_true")
    args = parser.parse_args()

    try:
        status = main(filename=args.exp_spec_name,
                      generate_seed=args.seed)
    except (RuntimeError, IOError) as e:
        print "Error: %s" % e
        status = 1
    sys.exit(status)
