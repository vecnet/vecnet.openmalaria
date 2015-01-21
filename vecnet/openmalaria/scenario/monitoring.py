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
from xml.etree.ElementTree import Element
from vecnet.openmalaria.scenario.core import attribute, Section, section


class AgeGroup(Section):
    @property
    @attribute
    def lowerbound(self):
        return "lowerbound", float

    @property
    def group(self):
        """
        :rtype: list
        """
        lowerbound = self.lowerbound
        age_group_list = []
        for age_group in self.et.findall("group"):
            upperbound = age_group.attrib["upperbound"]
            try:
                poppercent = age_group.attrib["poppercent"]
            except KeyError:
                poppercent = None
            age_group_list.append({"lowerbound": lowerbound,
                                   "upperbound": upperbound,
                                   "poppercent": poppercent})
            lowerbound = upperbound
        return age_group_list


class Monitoring(Section):
    @property
    @section
    def ageGroup(self):
        """
        :rtype: ageGroup
        """
        return AgeGroup

    @property  # name
    @attribute
    def name(self):
        return "name", str  # return the name of xml attribute for this property
    @name.setter
    def name(self, value):
        self.et.attrib["name"] = value

    @property  # continuous
    def continuous(self):
        """
        List of measures in <continuous> section
        Example: ["simulated EIR", "GVI coverage"]
        :rtype: list
        """
        list_of_measures = []
        if self.et.find("continuous") is None:
            return list_of_measures
        return self._get_measures(self.et.find("continuous"))
    @continuous.setter
    def continuous(self, list_of_measures):
        if self.et.find("continuous") is None:
            # Add continuous section
            self.et.append(Element("continuous"))
        self._replace_measures(self.et.find("continuous"), list_of_measures)

    @property  # SurveyOptions
    def SurveyOptions(self):
        """
        List of measures in <SurveyOpions> section
        Example: ["hHost", "nPatent", "nUncomp", "simulatedEIR", "nMassGVI"]
        :rtype: list
        """
        list_of_measures = []
        if self.et.find("SurveyOptions") is None:
            return list_of_measures
        return self._get_measures(self.et.find("SurveyOptions"))
    @SurveyOptions.setter
    def SurveyOptions(self, list_of_measures):
        if self.et.find("SurveyOptions") is None:
            # Add SurveyOptions section
            self.et.append(Element("SurveyOptions"))
        self._replace_measures(self.et.find("SurveyOptions"), list_of_measures)

    @property  # detectionLimit
    def detectionLimit(self):
        """
        Detection limit for parasitaemia
        Limit above which a human's infection is reported as patent
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#detection-limit-for-parasitaemia
        """
        surveys_elem = self.et.find("surveys")
        if surveys_elem is None:
            return None

        try:
            detectionLimit = float(surveys_elem.attrib["detectionLimit"])
        except KeyError:
            detectionLimit = None
        return detectionLimit
    @detectionLimit.setter
    def detectionLimit(self, value):
        surveys_elem = self.et.find("surveys")
        if surveys_elem is None:
            self.et.append(Element("surveys"))
            surveys_elem = self.et.find("surveys")

        surveys_elem.attrib["detectionLimit"] = value

    @property  # surveys
    def surveys(self):
        """
        Returns the list of timesteps when survey measures has been captured
        None if xml document is mailformed
        xpath: /scenario/monitoring/survey
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#survey-times-time-steps
        """
        survey_time_list = list()
        # Extract surveyTimes from /scenario/monitoring/surveys section
        # Using root element instead of xpath to avoid problems with namespaces
        # (root tag was <scenario> prior to schema 32, and then it was switched to <om:scenario>)
        try:
            for item in self.et.find("surveys").findall("surveyTime"):
                survey_time_list.append(int(item.text))
        except AttributeError:
            return None
        return survey_time_list
    @surveys.setter
    def surveys(self, list_of_survey_times):
        surveys_elem = self.et.find("surveys")
        if surveys_elem is None:
            # Add surveys section
            self.et.append(Element("surveys"))
            surveys_elem = self.et.find("surveys")

        for time in surveys_elem.findall("surveyTime"):
            surveys_elem.remove(time)

        for time in list_of_survey_times:
            tag = Element("surveyTime")
            tag.text = str(time)
            surveys_elem.append(tag)


    # Internal functions
    def _get_measures(self, et):
        """
        Get a list of measures in <continuous> or <SurveyOptions> section
        """
        list_of_measures = []
        for tag in et.findall("option"):
            if tag.attrib.get("value", "true") == "true":
                list_of_measures.append(tag.attrib["name"])
        return list_of_measures

    def _replace_measures(self, et, list_of_measures):
        """
        Build <continuous> or <SurveyOptions> section
        """
        for measure in et.findall("option"):
            et.remove(measure)

        for measure_name in list_of_measures:
            tag = Element("option")
            tag.attrib["name"] = measure_name
            tag.attrib["value"] = "true"
            et.append(tag)
