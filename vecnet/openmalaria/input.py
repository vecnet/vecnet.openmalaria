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
from collections import OrderedDict


class MonitoringSection:
    class Measures:
        def __init__(self, et):
            self.et = et  # ElementTree that represents continuous or SurveyOption sections in monitoring

        def _find_measure(self, measure):
            """
            Helper function for finding measure among <option> tags
            :returns: ElementTree object or None if measure is not found
            """
            survey_options = self.et
            for tag in survey_options:
                if tag.attrib["name"] == measure:
                    return tag
            return None

        def __getitem__(self, key):
            """Called to implement evaluation of self[key].
            Please refer to python documentation for additional details
            https://docs.python.org/2/reference/datamodel.html#object.__getitem__
            """
            tag = self._find_measure(key)
            if tag is None:
                raise KeyError()
            if tag.attrib["value"] == "true":
                return True
            return False

        def __setitem__(self, key, value):
            et = self._find_measure(key)
            if et is None:
                ElementTree.SubElement(self.et, "option", attrib={"name": key, value: str(value)})
            else:
                et.attrib["value"] = str(value)

        def __delitem__(self, key):
            et = self._find_measure(key)
            if et is not None:
                self.et.remove(et)
            else:
                raise KeyError()

        def __iter__(self):
            for measure in self.et.findall("option"):
                yield measure.attrib["name"]

    def __init__(self, et):
        self.et = et
        self.continuous = self.Measures(et.find("continuous"))
        self.SurveyOptions = self.Measures(et.find("SurveyOptions"))


class Vector:
    """
    https://code.google.com/p/openmalaria/wiki/XmlEntoVector
    """
    def __init__(self, et):
        self.name = et.attrib["mosquito"]
        # Mosquito parameters
        self.propInfected = float(et.attrib["propInfected"])
        self.propInfectious = float(et.attrib["propInfectious"])
        mosq = et.find("mosq")
        self.minInfectedThreshold = float(mosq.attrib["minInfectedThreshold"])
        self.mosqRestDuration = float(mosq.find("mosqRestDuration").attrib["value"])
        self.extrinsicIncubationPeriod = float(mosq.find("extrinsicIncubationPeriod").attrib["value"])
        self.mosqLaidEggsSameDayProportion = float(mosq.find("mosqLaidEggsSameDayProportion").attrib["value"])
        self.mosqSeekingDuration = float(mosq.find("mosqSeekingDuration").attrib["value"])
        self.mosqSurvivalFeedingCycleProbability = float(mosq.find("mosqSurvivalFeedingCycleProbability").attrib["value"])
        self.availabilityVariance = float(mosq.find("availabilityVariance").attrib["value"])
        #self.mosqProbBiting = mosq.find("mosqProbBiting").attrib["value"]
        #self.mosqProbFindRestSite = mosq.find("mosqProbFindRestSite").attrib["value"]
        #self.mosqProbResting = mosq.find("mosqProbResting").attrib["value"]
        self.mosqProbOvipositing = float(mosq.find("mosqProbOvipositing").attrib["value"])
        self.mosqHumanBloodIndex = float(mosq.find("mosqHumanBloodIndex").attrib["value"])

        # Mosquito seasonality
        self.seasonality = dict()
        self.seasonality["annualEIR"] = et.find("seasonality").attrib["annualEIR"]
        self.seasonality["smoothing"] = et.find("seasonality").find("monthlyValues").attrib["smoothing"]
        monthly_values = []
        for value in et.find("seasonality").find("monthlyValues"):
            monthly_values.append(value.text)
        self.seasonality["monthlyValues"] = monthly_values
        self.element_tree = et

        non_human_hosts = OrderedDict()
        # non Human hosts for this species
        # Using OrderedDict just in case if it will be necessary to preserve the order of nonHumanHosts
        for non_human_host in et.findall("nonHumanHosts"):
            non_human_hosts[non_human_host.attrib["name"]] = \
                {
                    "mosqRelativeEntoAvailability": non_human_host.find("mosqRelativeEntoAvailability").attrib["value"],
                    "mosqProbBiting": non_human_host.find("mosqProbBiting").attrib["value"],
                    "mosqProbFindRestSite": non_human_host.find("mosqProbFindRestSite").attrib["value"],
                    "mosqProbResting": non_human_host.find("mosqProbResting").attrib["value"],
                }

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

    @survey_timesteps.setter
    def survey_timesteps(self, list_of_survey_timesteps):
        """
        Update the list of timesteps when survey measures should be captured
        raises AttributeError if xml document is mailformed
        """
        # Clear <surveys> section
        self.root.find("monitoring").remove(self.root.find("monitoring").find("surveys"))
        # Create a new one and populate it with new timesteps
        surveys = ElementTree.SubElement(self.root.find("monitoring"), "surveys")
        for survey_timestep in list_of_survey_timesteps:
            survey_timestep_element = ElementTree.SubElement(surveys, "surveyTime")
            survey_timestep_element.text = str(survey_timestep)
        self.xml = ElementTree.tostring(self.root)

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
    def measure_has_age_group(cls, measure_id):
        if measure_id in ({7, 9, 21, 25, 26, 28, 29, 31, 32, 33, 34, 35, 36, 39, 40, 47, 48, 49, 50, 51, 54}):
            return False
        return True

    @classmethod
    def measure_has_species_name(cls, measure_id):
        if measure_id in ({31, 32, 33, 34}):
            return True
        return False

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