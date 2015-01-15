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
from vecnet.openmalaria.scenario.core import Section, attribute, tag_value, section


class Seasonality(Section):
    @property  # input
    @attribute
    def input(self):
        return "input", str

    @property  # annualEIR
    @attribute
    def annualEIR(self):
        return "annualEIR", float

    @property  # smoothing
    @tag_value
    def smoothing(self):
        """
        How the monthly values are converted into a daily sequence of values:
        1) none: no smoothing (step function)
        2) fourier: a Fourier series (with terms up to a2/b2) is fit to the sequence of monthly values and used to
        generate a smoothed list of daily values.

        type: string
        values: ("none" or "fourier")

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#smoothing-function
        """
        return "monthlyValues", "smoothing", str

    @property  # monthlyValues
    def monthlyValues(self):
        """
        Description of seasonality from monthly values. Multiple smoothing methods are possible
        (see smoothing attribute).
        List should contain twelve entries: January to December.
        :rtype: list

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#list-of-monthly-values
        """
        monthly_values = []
        for value in self.et.find("monthlyValues").findall("value"):
            monthly_values.append(float(value.text))
        return monthly_values
    @monthlyValues.setter
    def monthlyValues(self, monthly_values):
        tag = self.et.find("monthlyValues")
        # Remove all value tags from the monthlyValues section
        for node in tag.findall("value"):
            tag.remove(node)
        for value in monthly_values:
            element = Element("value")
            element.text = str(value)
            self.et.find("monthlyValues").append(element)

class Mosq(Section):
    @property  # minInfectedThreshold, double
    @attribute
    def minInfectedThreshold(self):
        """
        Mininum infected threshold for mosquitos
        If less than this many mosquitoes remain infected, transmission is interrupted.
        Type: double

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#mininum-infected-threshold-for-mosquitos
        """
        return "minInfectedThreshold", float

    @property
    @tag_value
    def mosqRestDuration(self):
        """
        Duration of the resting period of the vector (days)
        type: int

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#documentation-element-112
        """
        return "mosqRestDuration", "value", float


class Vector(Section):
    @property  # mosquito
    @attribute
    # Note this attribute is read only by design
    def mosquito(self):
        return "mosquito", str

    @property
    @attribute
    def propInfected(self):
        return "propInfected", float

    @property
    @attribute
    def propInfectious(self):
        return "propInfectious", float

    @property
    @section
    def seasonality(self):
        """
        :rtype: Seasonality
        """
        return Seasonality

    @property
    @section
    def mosq(self):
        """
        :rtype: Mosq
        """
        return Mosq

class Vectors():
    def __init__(self, et):
        self.et = et
        self.vectors = {}
        for anopheles in et.findall("anopheles"):
            self.vectors[anopheles.attrib["mosquito"]] = Vector(anopheles)

    def __getitem__(self, item):
        """
        :rtype: Vector
        """
        return self.vectors[item]

    def __setitem__(self, key, value):
        if isinstance(key, Vector):
            self.vectors[key] = value
        else:
            raise ValueError("only objects of Vector type are accepted")

    def __getattr__(self, item):
        """
        :rtype: Vector
        """
        if item in self.vectors:
            return self.vectors[item]
        raise AttributeError

    def __iter__(self):
        pass

class Entomology(Section):
    @property  # name
    @attribute
    def name(self):
        return "name", str

    @property  # mode
    @attribute
    def mode(self):
        return "mode", str

    @property  # scaledAnnualEIR
    @attribute
    def scaledAnnualEIR(self):
        return "scaledAnnualEIR", float

    @property
    def vectors(self):
        return Vectors(self.et.find("vector"))