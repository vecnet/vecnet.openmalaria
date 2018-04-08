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
import six

from vecnet.openmalaria.scenario.core import attribute, Section, section, attribute_setter
from vecnet.openmalaria.scenario.demography import Demography
from vecnet.openmalaria.scenario.entomology import Entomology
from vecnet.openmalaria.scenario.healthsystem import HealthSystem
from vecnet.openmalaria.scenario.interventions import Interventions
from vecnet.openmalaria.scenario.monitoring import Monitoring


class Scenario(Section):
    @property
    @section
    def monitoring(self):
        """
        :returns: Monitoring section
        :rtype: Monitoring
        """
        return Monitoring

    @property
    @section
    def demography(self):
        """
        :rtype: Demography
        """
        return Demography

    @property
    @section
    def healthSystem(self):
        """
        :rtype: HealthSystem
        """
        return HealthSystem

    @property
    @section
    def entomology(self):
        """
        :rtype: Entomology
        """
        return Entomology

    @property
    @section
    def interventions(self):
        """
        :retype: Interventions
        """
        return Interventions

    @property
    @attribute
    def name(self):
        """
        Name of the scenario
        :rtype: str
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#name-of-intervention
        """
        return "name", str
    @name.setter
    def name(self, name):
        assert isinstance(name, six.string_types)
        self.et.attrib["name"] = name

    @property
    @attribute
    def schemaVersion(self):
        """
        Version of xml schema.
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#version-of-the-xml-schema
        """
        return "schemaVersion", int

    @property
    @attribute
    def analysisNo(self):
        """
        :returns: Reference number of the analysis
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#version-of-the-xml-schema
        """
        return "analysisNo", int
    @analysisNo.setter
    @attribute_setter(attrib_type=int)
    def analysisNo(self, value):
        pass  # attribute_setter decorator will change analysisNo attribute

    @property
    @attribute
    def wuID(self):
        """
        Work unit identifier
        https://github.com/SwissTPH/openmalaria/wiki/GeneratedSchema32Doc#work-unit-identifier
        """
        return "wuID", int
    @wuID.setter
    @attribute_setter(attrib_type=int)
    def wuID(self, value):
        pass  # attribute_setter decorator will change wuID attribute

    @property
    def xml(self):
        if self.schemaVersion < 32:
            ElementTree.register_namespace("", "http://openmalaria.org/schema/scenario_32")
        else:
            ElementTree.register_namespace("om", "http://openmalaria.org/schema/scenario_32")

        if six.PY3:
            data = ElementTree.tostring(self.root, encoding="unicode")
        else:
            data = ElementTree.tostring(self.root)
        return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + data

    def __init__(self, xml):
        # self.xml = xml
        # Parsed xml file (as ElementTree)
        self.root = ElementTree.fromstring(xml)
        super(self.__class__, self).__init__(self.root)

    def __str__(self):
        return self.name

    def load_xml(self, xml):
        # self.xml = xml
        # Parsed xml file (as ElementTree)
        self.root = ElementTree.fromstring(xml)
        super(self.__class__, self).__init__(self.root)
