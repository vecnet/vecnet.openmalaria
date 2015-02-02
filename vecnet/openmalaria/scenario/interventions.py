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
from vecnet.openmalaria.scenario.core import Section, attribute, attribute_setter
from vecnet.openmalaria.scenario.healthsystem import HealthSystem


class HumanInterventions(Section):
    pass

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
        if self.et.find("changeHS") is None:
            return health_systems
        for health_system in self.et.find("changeHS").findall("timedDeployment"):
            health_systems.append([int(health_system.attrib("time")), HealthSystem(self.et)])
        return health_systems

    @property  # changeEIR
    def changeEIR(self):
        if self.et.find("changeEIR") is None:
            return None
        eir_daily = []
        for value in self.et.find("changeEIR").findall("EIRDaily"):
            eir_daily.append(float(value.text))
        return eir_daily

    @property  # human
    def human(self):
        return HumanInterventions(self.et.find("human"))

    def __getattr__(self, item):
        raise KeyError


class Intervention(Section):
    pass

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


class ITN(Intervention):
    def __init__(self, et):
        super(self.__class__, self).__init__(et)
        self.id = self.et.attrib["id"]
        self.name = self.et.attrib.get("name", None)

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
        return float(self.et.find("ITN").find("usage").attrib["value"])
    @usage.setter
    def usage(self, value):
        assert isinstance(value, float)
        self.et.find("ITN").find("usage").attrib["value"] = value

    @property
    # Same approach as with scenario.entomology.vectors may work here too
    def anophelesParams(self):
        """
        :rtype: AnophelesParams
        """
        list_of_anopheles = []
        for anophelesParams in self.et.find("ITN").findall("anophelesParams"):
            list_of_anopheles.append(AnophelesParams(anophelesParams))
        return list_of_anopheles

    def get_attrition_in_years(self):
        """
        Function for the Basic UI
        """
        function = self.et.find("ITN").find("attritionOfNets").attrib["function"]
        if function != "step":
            return None
        L = self.et.find("ITN").find("attritionOfNets").attrib["L"]
        return L

    def set_attrition_in_years(self, years):
        self.et.find("ITN").find("attritionOfNets").attrib["function"] = "step"
        self.et.find("ITN").find("attritionOfNets").attrib["L"] = years