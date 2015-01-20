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
from vecnet.openmalaria.scenario.core import Section, tag_value, tag_value_setter, attribute, section

__author__ = 'Alexander'


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


class HealthSystem(Section):
    @property
    @section
    def ImmediateOutcomes(self):
        """
        :rtype: ImmediateOutcomes
        """
        return ImmediateOutcomes
