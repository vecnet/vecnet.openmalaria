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


class Vector:
    """
    https://code.google.com/p/openmalaria/wiki/XmlEntoVector
    """
    def __init__(self, et):
        self.name = et.attrib["mosquito"]
        # Mosquito seasonality
        self.seasonality = dict()
        self.seasonality["annualEIR"] = et.find("seasonality").attrib["annualEIR"]
        self.seasonality["smoothing"] = et.find("seasonality").find("monthlyValues").attrib["smoothing"]
        monthly_values = []
        for value in et.find("seasonality").find("monthlyValues"):
            monthly_values.append(value.text)
        self.seasonality["monthlyValues"] = monthly_values
        self.element_tree = et

    def __str__(self):
        return self.name


class XmlInputFile(object):
    def __init__(self, xml):
        """
        xml - string, contents of xml file or open file handle
        """
        if hasattr(xml, "read"):
            self.xml = xml.read()
        else:
            self.xml = xml
        try:
            self.root = ElementTree.fromstring(self.xml)
        except ParseError:
            raise RuntimeError("Can't parse xml file")
        self.schemaVersion = self.root.attrib.get("schemaVersion", None)

    @property
    def monitoring_age_groups(self):
        """
        :returns: List of age groups in monitoring/ageGroup section.
        AgeGroup is represented as a dictionary with two keys - "lowerbound" and "upperbound"
        """
        return self._get_age_groups(self.root.find("monitoring").find("ageGroup"))

    @property
    def demography_age_groups(self):
        """
        :returns: List of age groups in monitoring/ageGroup section.
        AgeGroup is represented as a dictionary with two keys - "lowerbound" and "upperbound"
        """
        return self._get_age_groups(self.root.find("demography").find("ageGroup"))

    @property
    def survey_timesteps(self):
        """
        Returns the list of timesteps when survey measures has been captured
        None if xml document is mailformed
        """
        survey_time_list = list()
        # Extract surveyTimes from /scenario/monitoring/surveys section
        # Using root element instead of xpath to avoid problems with namespaces
        # (root tag was <scenario> prior to schema 32, and then it was switched to <om:scenario>)
        try:
            for item in self.root.find("monitoring").find("surveys").findall("surveyTime"):
                survey_time_list.append(int(item.text))
        except AttributeError:
            return None
        return survey_time_list

    @property
    def vectors(self):
        """
        Returns a list of vectors in a scenario file or None if non-vector model is used
        """
        vectors = []
        try:
            for mosquito in self.root.find("entomology").find("vector").findall("anopheles"):
                vectors.append(Vector(mosquito))
        except AttributeError:
            return None
        return vectors

    #@property
    # def interventions(self):
    #     # https://code.google.com/p/openmalaria/wiki/ModelInterventions
    #     try:
    #         root = ElementTree.fromstring(self.xml)
    #     except ParseError:
    #         return None
    #
    #     interventions = []
    #     try:
    #         change_eir = root.find("interventions").find("changeEIR")
    #         interventions.append({"type": "changeEIR", "name": change_eir.attrib["name"]})
    #     except AttributeError:
    #         # No changeEIR intervention defined
    #         pass
    #
    #     try:
    #         human = root.find("interventions").find("human")
    #     except AttributeError:
    #         # No human-targeted intervention defined
    #         pass

    @classmethod
    def _get_age_groups(cls, section):
        """
        AgeGroup structure is the same in monitoring and demographics section, so we can use one function to parse both
        """
        age_group_list = list()
        lowerbound = section.attrib["lowerbound"]
        for age_group in section.findall("group"):
            upperbound = age_group.attrib["upperbound"]
            age_group_list.append({"lowerbound": lowerbound,
                                   "upperbound": upperbound})
            lowerbound = upperbound
        return age_group_list
