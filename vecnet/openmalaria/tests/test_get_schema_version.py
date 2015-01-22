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

from vecnet.openmalaria import get_schema_version_from_xml


class TestGetSchemaVersion(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_schema_version_from_xml(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # use file handle as input to get_schema_version_from_xml
        with open(os.path.join(base_dir, os.path.join("get_schema_version_from_xml", "scenario30.xml"))) as fp:
            schema_version = get_schema_version_from_xml(fp)
            self.assertEqual(schema_version, "30")

        # Use content of xml file (string) as an input to get_schema_version_from_xml
        with open(os.path.join(base_dir, os.path.join("get_schema_version_from_xml", "scenario30.xml"))) as fp:
            schema_version = get_schema_version_from_xml(fp.read())
            self.assertEqual(schema_version, "30")
        with open(os.path.join(base_dir, os.path.join("get_schema_version_from_xml", "scenario32.xml"))) as fp:
            schema_version = get_schema_version_from_xml(fp.read())
            self.assertEqual(schema_version, "32")
        with open(os.path.join(base_dir, os.path.join("get_schema_version_from_xml", "non_om_xml.xml"))) as fp:
            schema_version = get_schema_version_from_xml(fp.read())
            self.assertIsNone(schema_version)
        # Test empty string
        schema_version = get_schema_version_from_xml("")
        self.assertIsNone(schema_version)

        # Test non-xml string
        schema_version = get_schema_version_from_xml("abcdef")
        self.assertIsNone(schema_version)


if __name__ == "__main__":
    unittest.main()
