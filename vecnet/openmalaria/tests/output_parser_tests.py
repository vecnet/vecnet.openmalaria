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

from vecnet.openmalaria.output_parser import OutputParser
import unittest


class TestOutputParser(unittest.TestCase):
    def test_output_parser(self):
        output_parser = OutputParser(open("output_parser\\scenario.xml"),
                                     survey_output_file=open("output_parser\\output.txt"),
                                     cts_output_file=open("output_parser\\ctsout.txt"))
        self.assertEqual(output_parser.survey_time_list, [730, 803, 876, 949, 1022, 1095])
        self.assertEqual(output_parser.get_cts_measures(), ["simulated EIR"])
        self.assertEqual(len(output_parser.cts_output_data["simulated EIR"]), 1096)
        self.assertEqual(set(output_parser.get_survey_measures()), ({[(3, 2), (3, 1), (14, 1), (14, 2)]}))
        measure_names = set()
        for measure in output_parser.get_survey_measures():
            measure_names.add(output_parser.get_survey_measure_name(measure_id=measure[0],
                                                                    third_dimension=measure[1]))
        self.assertEqual(measure_names,
                         ({["nPatent(18 - 90)", "nPatent(0 - 18)", "nUncomp(0 - 18)", "nUncomp(18 - 90)"]}))
        self.assertEqual(output_parser.survey_output_data,
                         {(3, 2): [[730, 16.0], [803, 17.0], [876, 16.0], [949, 14.0], [1022, 12.0], [1095, 10.0]],
                          (3, 1): [[730, 27.0], [803, 16.0], [876, 15.0], [949, 23.0], [1022, 20.0], [1095, 13.0]],
                          (14, 1): [[730, 1116.0], [803, 99.0], [876, 82.0], [949, 100.0], [1022, 102.0], [1095, 92.0]],
                          (14, 2): [[730, 280.0], [803, 21.0], [876, 26.0], [949, 28.0], [1022, 13.0], [1095, 24.0]]}
                         )

    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()
