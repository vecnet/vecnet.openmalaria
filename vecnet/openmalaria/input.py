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

from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError


class XmlInputFile:
    def __init__(self, xml):
        if hasattr(xml, "read"):
            self.xml = xml.read()
        else:
            self.xml = xml

    @property
    def monitoring_age_groups(self):
        """
        :returns: List of age groups in monitoring/ageGroup section.
        AgeGroup is represented as a dictionary with two keys - "lowerbound" and "upperbound"
        """
        root = ElementTree.fromstring(self.xml)
        return self._get_age_groups(root.find("monitoring").find("ageGroup"))

    @property
    def demography_age_groups(self):
        """
        :returns: List of age groups in monitoring/ageGroup section.
        AgeGroup is represented as a dictionary with two keys - "lowerbound" and "upperbound"
        """
        root = ElementTree.fromstring(self.xml)
        return self._get_age_groups(root.find("demography").find("ageGroup"))

    @property
    def survey_timesteps(self):
        """
        Returns the list of timesteps when survey measures has been captured
        None if xml document is mailformed
        """
        try:
            root = ElementTree.fromstring(self.xml)
        except ParseError:
            return None

        survey_time_list = list()
        # Extract surveyTimes from /scenario/monitoring/surveys section
        # Using root element instead of xpath to avoid problems with namespaces
        # (root tag was <scenario> prior to schema 32, and then it was switched to <om:scenario>)
        try:
            for item in root.find("monitoring").find("surveys").findall("surveyTime"):
                survey_time_list.append(int(item.text))
        except AttributeError:
            return None
        return survey_time_list

    def _get_age_groups(self, section):
        age_group_list = list()
        lowerbound = section.attrib["lowerbound"]
        for age_group in section.findall("group"):
            upperbound = age_group.attrib("upperbound")
            age_group.append({"lowerbound":lowerbound,
                              "upperbound": upperbound})
            lowerbound = upperbound
        return age_group_list
