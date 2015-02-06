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
from vecnet.openmalaria.scenario.core import Section, attribute, tag_value, section, attribute_setter, tag_value_setter


class Seasonality(Section):
    @property  # input
    @attribute
    def input(self):
        return "input", str

    @property  # annualEIR
    @attribute
    def annualEIR(self):
        """
        Annual EIR
        If this attribute is included, EIR for this species is scaled to this level. Note that if the scaledAnnualEIR
        attribute of the entomology element is also used, EIR is scaled again, making this attribute the EIR relative
        to other species.

        With some seasonality inputs, this attribute is optional, in which case (if scaledAnnualEIR is also not
        specified) transmission depends on all parameters of the vector. With some seasonality inputs, however, this
        parameter must be specified.

        Units: Inoculations (the number of bites by infectious mosquitoes) per adult per annum
        Type: float
        Min: 0

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#annual-eir
        """
        return "annualEIR", float
    @annualEIR.setter
    @attribute_setter(attrib_type=float)
    def annualEIR(self, value):
        pass  # attribute_setter decorator will change annualEIR attribute

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

    @property
    @tag_value
    def mosqHumanBloodIndex(self):
        """
        Human blood index
        The proportion of resting mosquitoes which fed on human blood during the last feed.

        type: double
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#documentation-element-122
        """
        return "mosqHumanBloodIndex", "value", float
    @mosqHumanBloodIndex.setter
    @tag_value_setter(tag="mosqHumanBloodIndex", attrib="value")
    def mosqHumanBloodIndex(self, value):
        pass  # mosqHumanBloodIndex parameter will be set by tag_value_setter decorator

class Vector(Section):
    """
    Class that represents /scenario/entomology/vector/anopheles section
    https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#anopheles-n2
    """
    @property  # mosquito
    @attribute
    def mosquito(self):
        """
        Identifier for this anopheles species
        type: string

        :rtype: str
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#identifier-for-this-anopheles-species
        """
        return "mosquito", str
    @mosquito.setter
    @attribute_setter(attrib_type=(str, unicode))
    def mosquito(self, value):
        pass  # attribute_setter decorator will change mosquito attribute

    @property  # propInfected
    @attribute
    def propInfected(self):
        """
        Initial estimate of proportion of mosquitoes infected (ρ_O)
        Initial guess of the proportion of mosquitoes which are infected, o: O_v(t) = o*N_v(t).
        Only used as a starting value.

        type: float
        units: Proportion

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#anopheles-n2
        """
        return "propInfected", float
    @propInfected.setter
    @attribute_setter(attrib_type=float)
    def propInfected(self, value):
        pass  # attribute_setter decorator will change propInfected attribute

    @property  # propInfectious
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

    def add(self, vector, InterventionAnophelesParams = None):
        """
        Add a vector to entomology section.
        vector is either ElementTree or xml snippet

        InterventionAnophelesParams is an anophelesParams section for every GVI, ITN and IRS intervention
        already defined in the scenario.xml

        """
        # TODO
        # 1. If there are GVI interventions, for every GVI, add anophelesParams section.
        # (gvi_anophelesParams field in AnophelesSnippets models)
        # 2. If there are ITN interventions, for every ITN, add anophelesParams section
        # (itn_anophelesParams field in AnophelesSnippets models)
        # 3. If there are IRS interventions, for every IRS section add anophelesParams section
        # (irs_anophelesParams field in AnophelesSnippets models)

        assert isinstance(vector, (str, unicode))
        et = ElementTree.fromstring(vector)
        # check if it is valid vector
        mosquito = Vector(et)
        assert isinstance(mosquito.mosquito, str)
        assert isinstance(mosquito.propInfected, float)
        assert len(mosquito.seasonality.monthlyValues) == 12
        self.et.append(et)

    @property
    def vectors(self):
        """
        :rtype: dict
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
        # TODO:
        #  1. For every GVI intervention, remove respective anophelesParams section
        #  2. For every ITN intervention, remove respective anophelesParams section
        #  3. For every IRS intervention, remove respective anophelesParams section
        for anopheles in self.et.findall("anopheles"):
            if anopheles.attrib['mosquito'] == key:
                self.et.remove(anopheles)
                return
        raise KeyError(key)

    def __iter__(self):
        """
        Iterator function. Allows using scenario.entomology.vectors in for statement
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
        """
        Override annual EIR
        If set, the annual EIR (for all species of vector) is scaled to this level; can be omitted if not needed.

        Units: Infectious bits per adult per year
        Type: double

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#override-annual-eir
        """
        return "scaledAnnualEIR", float
    @scaledAnnualEIR.setter
    @attribute_setter(attrib_type=float)
    def scaledAnnualEIR(self, value):
        pass  # attribute_setter decorator will change scaledAnnualEIR attribute

    @property
    def vectors(self):
        return Vectors(self.et.find("vector"))

    def __str__(self):
        return self.name