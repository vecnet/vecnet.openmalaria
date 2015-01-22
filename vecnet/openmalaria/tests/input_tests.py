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

import unittest
import os

from vecnet.openmalaria.input import XmlInputFile


class TestXmlInputFile(unittest.TestCase):
    def setUp(self):
        pass

    def test_survey_timesteps_property(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        xml_file = XmlInputFile(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))))
        self.assertEqual(xml_file.survey_timesteps, [730, 736, 742, 748])
        self.assertEqual([vector.name for vector in xml_file.vectors], ["gambiae"])
        xml_file = XmlInputFile(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c_no_surveys.xml"))))
        self.assertEqual(xml_file.survey_timesteps, [])
        xml_file = XmlInputFile("<xml></xml>")
        self.assertIsNone(xml_file.survey_timesteps)
        self.assertRaises(RuntimeError, XmlInputFile, "...")
        #self.assertIsNone(xml_file.survey_timesteps)

if __name__ == "__main__":
    unittest.main()
