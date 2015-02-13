#!/bin/env python2
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
from vecnet.openmalaria.scenario.core import Section, attribute, attribute_setter, section, tag_value
from vecnet.openmalaria.scenario.healthsystem import HealthSystem


class Interventions(Section):
    """
    Inverventions section in OpenMalaria xml input file
    https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#preventative-interventions
    """
    @property  # changeHS
    def changeHS(self):
        """
        Change health system interventions
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#change-health-system
        Returns: list of HealthSystems together with timestep when they are applied
        """
        health_systems = []
        change_hs = self.et.find("changeHS")
        if change_hs is None:
            return health_systems
        for health_system in change_hs.findall("timedDeployment"):
            health_systems.append([int(health_system.attrib("time")), HealthSystem(self.et)])
        return health_systems

    @property  # changeEIR
    def changeEIR(self):
        change_eir = self.et.find("changeEIR")
        if change_eir is None:
            return None
        eir_daily = []
        for value in change_eir.findall("EIRDaily"):
            eir_daily.append(float(value.text))
        return eir_daily

    @property  # human
    def human(self):
        return HumanInterventions(self.et.find("human"))

    def __getattr__(self, item):
        raise KeyError


class Component(Section):
    @property  # name
    @attribute
    def name(self):
        """
        An informal name/description of the intervention

        :rtype: str
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#name-of-component
        """
        return "name", str
    @name.setter
    @attribute_setter(attrib_type=str)
    def name(self, value):
        pass   # value of name attribute will be set by attribute_setter decorator

class AnophelesParams(Section):
    """
    Parameters of mosquitos affected by this ITN intervention

    https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#anophelesparams
    """
    @property
    @attribute
    def mosquito(self):
        """
        Name of the affected anopheles-mosquito species.

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#anophelesparams
        """
        return "mosquito", str
    @mosquito.setter
    @attribute_setter(attrib_type=str)
    def mosquito(self, value):
        pass

    @property
    @attribute
    def propActive(self):
        """
        Proportion of bites for which net acts

        The proportion of bites, when nets are in use, for which the net has any action whatsoever on the mosquito.
        At the moment this is constant across humans and deterministic: relative attractiveness and survival factors
        are base(1-usagepropActing) + intervention_factorusagepropActing.
        See also "usage" (proportion of time nets are used by humans).

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#proportion-of-bites-for-which-net-acts
        """
        return "propActive", float
    @propActive.setter
    @attribute_setter(attrib_type=float)
    def propActive(self, value):
        pass

    @property
    @tag_value
    def deterrency(self):
        return "deterrency", "value", float

    @property
    @tag_value
    def preprandialKillingEffect(self):
        return "preprandialKillingEffect", "value", float

    @property
    @tag_value
    def postprandialKillingEffect(self):
        return "postprandialKillingEffect", "value", float


class ITN(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.itn = et.find("ITN")
        self.id = self.et.attrib["id"]

    @property  # usage
    def usage(self):
        """
        Proportion of time nets are used by humans

        At the moment this is constant across humans and deterministic: relative attractiveness and survival factors
        are base(1-usagepropActing) + intervention_factorusagepropActing.
        See also "propActing" (proportion of bits for which net acts).

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#proportion-of-time-nets-are-used-by-humans
        :rtype: float
        """
        return float(self.itn.find("usage").attrib["value"])
    @usage.setter
    def usage(self, value):
        assert isinstance(value, float)
        self.itn.find("usage").attrib["value"] = value

    @property
    # Same approach as with scenario.entomology.vectors may work here too
    def anophelesParams(self):
        """
        :rtype: AnophelesParams
        """
        list_of_anopheles = []
        for anophelesParams in self.itn.findall("anophelesParams"):
            list_of_anopheles.append(AnophelesParams(anophelesParams))
        return list_of_anopheles

    def get_attrition_in_years(self):
        """
        Function for the Basic UI
        """
        attrition_of_nets = self.itn.find("attritionOfNets")
        function = attrition_of_nets.attrib["function"]
        if function != "step":
            return None
        L = attrition_of_nets.attrib["L"]
        return L

    def set_attrition_in_years(self, years):
        attrition_of_nets = self.itn.find("attritionOfNets")
        attrition_of_nets.attrib["function"] = "step"
        attrition_of_nets.attrib["L"] = years

class Decay(Section):
    """
    Description of decay of all intervention effects. Documentation:
    see DecayFunction type or http://code.google.com/p/openmalaria/wiki/ModelDecayFunctions

    https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#decay-n4
    """
    @property
    @attribute
    def function(self):
        return "function", str

    @property
    @attribute
    def L(self):
        return "L", float

    @property
    @attribute
    def k(self):
        return "k", float

    @property
    @attribute
    def mu(self):
        return "mu", float

    @property
    @attribute
    def sigma(self):
        return "sigma", float

class GVI(Component):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.gvi = et.find("GVI")

    @property
    def decay(self):
        """
        :rtype: Decay
        """
        return Decay(self.gvi.find("decay"))

    @property
    # Same approach as with scenario.entomology.vectors may work here too
    def anophelesParams(self):
        """
        :rtype: AnophelesParams
        """
        list_of_anopheles = []
        for anophelesParams in self.gvi.findall("anophelesParams"):
            list_of_anopheles.append(AnophelesParams(anophelesParams))
        return list_of_anopheles


class HumanInterventions(Section):
    """
    List of human interventions
    """

    @property
    def components(self):
        human_interventions = {}
        for component in self.et.findall("component"):
            if component.find("ITN") is not None:
                human_interventions[component.attrib["id"]] = ITN(component)
            if component.find("GVI") is not None:
                human_interventions[component.attrib["id"]] = GVI(component)
        return human_interventions

    def __getitem__(self, item):
        """
        :rtype: Intervention
        """
        return self.components[item]

    def __getattr__(self, item):
        """
        :rtype: Intervention
        """
        return self.components[item]

    def __len__(self):
        return len(self.components)

    def __iter__(self):
        """
        Iterator function. Allows using scenario.interventions.human in for statement
        i.e.
        for intervention in scenario.interventions.human:
           print intervention.name

        :rtype: Vector
        """
        for intervention_name, intervention in self.components.iteritems():
            yield intervention
