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
from xml.etree import ElementTree
from vecnet.openmalaria.scenario.core import Section, attribute, tag_value, section, attribute_setter


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
        return "mosqRestDuration", "value", int


class Vector(Section):
    @property  # mosquito
    @attribute
    def mosquito(self):
        return "mosquito", str
    @mosquito.setter
    @attribute_setter
    def mosquito(self, value):
        pass

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
 #       assert isinstance(et, ElementTree)
        self.et = et

    def add(self, vector):
        """
        Add a vector to entomology section.
        vector is either ElementTree or xml snippet
        """
        assert isinstance(vector, (str, unicode))
        et = ElementTree.fromstring(vector)
        # check if it is valid vector
        mosquito = Vector(et)
        assert(isinstance(mosquito.mosquito, str))
        assert(isinstance(mosquito.propInfected, float))
        assert(len(mosquito.seasonality.monthlyValues), 12)
        self.et.append(et)

    @property
    def vectors(self):
        """
        :rtype: list
        """
        vectors = {}
        for anopheles in self.et.findall("anopheles"):
            vectors[anopheles.attrib["mosquito"]] = Vector(anopheles)
        return vectors

    def __getitem__(self, item):
        """
        :rtype: Vector
        """
        return self.vectors[item]

    def __getattr__(self, item):
        """
        :rtype: Vector
        """
        return self.vectors[item]

    def __len__(self):
        return len(self.vectors)

    def __delitem__(self, key):
        for anopheles in self.et.findall("anopheles"):
            if anopheles.attrib['mosquito'] == key:
                self.et.remove(anopheles)
                return
        raise KeyError(key)

    def __iter__(self):
        """
        Interator function. Allows using scenario.entomology.vectors in for statement
        i.e.
        for vector in scenario.entomology.vectors:
           print vector.mosquito

        :rtype: Vector
        """
        for vector in self.vectors:
            yield self.vectors[vector]

    def __str__(self):
        return self.mosquito

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

    def __str__(self):
        return self.name