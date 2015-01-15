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
from vecnet.openmalaria.scenario.core import Section, attribute, section
from vecnet.openmalaria.scenario.monitoring import AgeGroup


class Demography(Section):
    @property  # maximumAgeYrs (double)
    @attribute
    def maximumAgeYrs(self):
        """
        Maximum age of simulated humans
        Units: Years Min: 0 Max: 100

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#maximum-age-of-simulated-humans
        """
        return "maximumAgeYrs", float
    @maximumAgeYrs.setter
    def maximumAgeYrs(self, value):
        assert isinstance(value, (int, float))
        self.et.attrib["maximumAgeYrs"] = str(value)

    @property  # name (string)
    @attribute
    def name(self):
        """
        Name of the demography data

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#attributes-1
        """
        return "name", str
    @name.setter
    def name(self, value):
        self.et.attrib["name"] = value

    @property  # popSize (int)
    @attribute
    def popSize(self):
        """
        Population size
        Units: Count Min: 1 Max: 100000

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#population-size
        """
        return "popSize", int
    @popSize.setter
    def popSize(self, value):
        self.et.attrib["popSize"] = value

    @property  # growthRate (double)
    @attribute
    def growthRate(self):
        """
        Growth rate of human population. (we should be able to implement this with non-zero values)
        Units: Number Min: 0 Max: 0

        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#growth-rate-of-human-population
        """
        return "growthRate", float

    @property  # ageGroup
    @section
    def ageGroup(self):
        """
        List of age groups included in demography
        :rtype: AgeGroup
        https://github.com/vecnet/om_schema_docs/wiki/GeneratedSchema32Doc#age-groups
        """
        return AgeGroup
