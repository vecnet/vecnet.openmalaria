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

from vecnet.openmalaria.scenario.core import Section, tag_value, tag_value_setter, attribute, attribute_setter, section

__author__ = 'Alexander'


class Drug():
    def __init__(self, et, name):
        self.et = et
        self.name = name

    @property
    def initialACR(self):
        return float(self.et.find("initialACR").find(self.name).attrib["value"])
    @initialACR.setter
    def initialACR(self, value):
        assert isinstance(value, (int, float))
        self.et.find("initialACR").find(self.name).attrib["value"] = str(value)

    @property
    def compliance(self):
        return float(self.et.find("compliance").find(self.name).attrib["value"])
    @compliance.setter
    def compliance(self, value):
        assert isinstance(value, (int, float))
        self.et.find("compliance").find(self.name).attrib["value"] = str(value)

    @property
    def nonCompliersEffective(self):
        return float(self.et.find("nonCompliersEffective").find(self.name).attrib["value"])
    @nonCompliersEffective.setter
    def nonCompliersEffective(self, value):
        assert isinstance(value, (int, float))
        self.et.find("nonCompliersEffective").find(self.name).attrib["value"] = str(value)


class Drugs():
    drug_tag_dict = {
        "CQ": "",
        "SP": "CQ",
        "AQ": "SP",
        "SPAQ": "AQ",
        "ACT": "SPAQ",
        "QN": "ACT",
        "selfTreatment": "QN"
    }

    def __init__(self, et):
        self.et = et

    def add(self, name, value, sections):
        assert isinstance(name, (str, unicode))
        drug = ElementTree.Element(name)
        drug.attrib["value"] = str(value)

        tag = self.drug_tag_dict[name]

        index_prior = -1
        for section in sections:
            elem_list = self.et.find(section)

            for el in elem_list:
                if el.tag == tag:
                    index_prior = elem_list.index(el)
                    if elem_list[index_prior + 1].tag == name:
                        break
                    elem_list.insert(index_prior + 1, drug)

    @property
    def drugs(self):
        drugs = {}

        if self.et is None:
            return drugs

        for elem in self.et.find("initialACR"):
            drugs[elem.tag] = Drug(self.et, elem.tag)

        for elem in self.et.find("compliance"):
            if elem.tag not in drugs:
                drugs[elem.tag] = Drug(self.et, elem.tag)

        for elem in self.et.find("nonCompliersEffective"):
            if elem.tag not in drugs:
                drugs[elem.tag] = Drug(self.et, elem.tag)

        return drugs

    def __getitem__(self, item):
        """
        :rtype: Drug
        """
        return self.drugs[item]

    def __getattr__(self, item):
        """
        :rtype: Drug
        """
        return self.drugs[item]

    def __len__(self):
        return len(self.drugs)

    # def __delitem__(self, key):
    #     # TODO:
    #     pass

    def __iter__(self):
        """
        Iterator function. Allows using scenario.healthSystem.ImmediateOutcomes.drugs in for statement
        i.e.
        for drug in scenario.healthSystem.ImmediateOutcomes.drugs:
           print drug.name

        :rtype: Drug
        """
        for drug in self.drugs:
            yield self.drugs[drug]

    def __str__(self):
        return self.name


class ImmediateOutcomes(Section):
    @property
    @attribute
    def name(self):
        return "name", str

    @property  # pSeekOfficialCareUncomplicated1
    def pSeekOfficialCareUncomplicated1(self):
        return float(self.et.find("pSeekOfficialCareUncomplicated1").attrib["value"])

    @pSeekOfficialCareUncomplicated1.setter
    def pSeekOfficialCareUncomplicated1(self, value):
        assert isinstance(value, (int, float))
        self.et.find("pSeekOfficialCareUncomplicated1").attrib["value"] = str(value)

    @property  # pSeekOfficialCareUncomplicated2
    def pSeekOfficialCareUncomplicated2(self):
        return float(self.et.find("pSeekOfficialCareUncomplicated2").attrib["value"])

    @pSeekOfficialCareUncomplicated2.setter
    def pSeekOfficialCareUncomplicated2(self, value):
        assert isinstance(value, (int, float))
        self.et.find("pSeekOfficialCareUncomplicated2").attrib["value"] = str(value)

    @property  # pSelfTreatUncomplicated
    def pSelfTreatUncomplicated(self):
        return float(self.et.find("pSelfTreatUncomplicated").attrib["value"])

    @pSelfTreatUncomplicated.setter
    def pSelfTreatUncomplicated(self, value):
        assert isinstance(value, (int, float))
        self.et.find("pSelfTreatUncomplicated").attrib["value"] = str(value)

    @property  # pSeekOfficialCareSevere
    def pSeekOfficialCareSevere(self):
        return float(self.et.find("pSeekOfficialCareSevere").attrib["value"])

    @pSeekOfficialCareSevere.setter
    def pSeekOfficialCareSevere(self, value):
        assert isinstance(value, (int, float))
        self.et.find("pSeekOfficialCareSevere").attrib["value"] = str(value)

    @property  # firstLine
    def firstLine(self):
        return self.et.find("drugRegimen").attrib["firstLine"]

    @firstLine.setter
    def firstLine(self, value):
        assert isinstance(value, (str, unicode))
        self.et.find("drugRegimen").attrib["firstLine"] = value

    @property  # secondLine
    @tag_value
    def secondLine(self):
        return "drugRegimen", "secondLine", str

    @secondLine.setter
    @tag_value_setter("drugRegimen", "secondLine")
    def secondLine(self, value):
        pass  # attribute modification is done in the tag_value_setter decorator

    @property  # inpatient
    @tag_value
    def inpatient(self):
        return "drugRegimen", "inpatient", str

    @inpatient.setter
    def inpatient(self, value):
        self.et.find("drugRegimen").attrib["inpatient"] = value

    @property
    def drugs(self):
        return Drugs(self.et)


class HealthSystem(Section):
    @property
    @section
    def ImmediateOutcomes(self):
        """
        :rtype: ImmediateOutcomes
        """
        return ImmediateOutcomes
