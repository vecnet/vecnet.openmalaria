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

import json
import re
from .helpers import prime_numbers


class Scenario:
    def __init__(self, xml, parameters=None):
        self.xml = xml
        self.parameters = parameters

    def __str__(self):
        return self.xml

    def __unicode__(self):
        return self.xml


class ExperimentSpecification:
    """
    OpenMalaria experiment specification is a json file. This class is an SDK for working with that file format.
    """
    def __init__(self, experiment):
        # Accept both json string and dictionary as an input. string is converted to dict automatically
        if isinstance(experiment, (str, unicode)):
            experiment = json.loads(experiment)
        if isinstance(experiment, file):
            experiment = json.load(experiment)
        if not isinstance(experiment, dict):
            raise TypeError("experiment should be either string or dict")

        self.experiment = experiment
        if "name" in self.experiment:
            self.name = self.experiment["name"]
        else:
            self.name = "Unnamed Experiment"

        if "basefile" in self.experiment:
            # Load baseline scenario from external file
            with open(self.experiment["basefile"]) as fp:
                self.experiment["base"] = fp.read()

    def __str__(self):
        return self.name

    def _apply_changes(self, scenario, sweep_name, arm_name):
        arm = self.experiment["sweeps"][sweep_name][arm_name]
        for param_change in arm:
            # arm substitution string should start and end with an @
            if re.match("^@.*@$", param_change) is None:
                raise TypeError("arm substitution string should start and end with an @, for example @param1@")
            # Each arm may contain more that one parameter
            # changes are applied in a random order currently
            param_value = arm[param_change]
            if isinstance(param_value, (int, float)):
                param_value = str(param_value)
            if param_value[0:7] == "file://":
                with open(param_value[7:], "r") as fp:
                    param_value = fp.read()

            scenario = scenario.replace(param_change, param_value)
        return scenario

    def _apply_combination(self, scenario, sweeps_applied, combination):
        for i in range(0, len(sweeps_applied)):
        # Apply sweeps in order defined by user
            sweep = sweeps_applied[i]
            arm = combination[i]
            scenario = self._apply_changes(scenario, sweep, arm)
        return scenario

    def scenarios(self, generate_seed=False):
        """
        Generator function. Spits out scenarios for this experiment
        """
        seed = prime_numbers(1000)
        sweeps_all = self.experiment["sweeps"].keys()
        if "combinations" in self.experiment:
            if isinstance(self.experiment["combinations"], list):
                # For backward compatibility with experiments1-4s
                combinations_in_experiment = {" ": self.experiment["combinations"]}
                #if self.experiment["combinations"] == []:
                #    # Special notation for fully-factorial experiments
                #    combinations_in_experiment = {" ":[[],[]]}
            else:
                # Combinations must be a dictionary in this particular case
                combinations_in_experiment = self.experiment["combinations"]
        else:
            # Support no combinations element:
            combinations_in_experiment = dict()    # empty dict 

        #1) calculate combinations_sweeps (depends on ALL combinations_ items)
        # Get the list of fully factorial sweeps
        all_combinations_sweeps = []
        all_combinations = []
        for key, combinations_ in combinations_in_experiment.items():
            # generate all permutations of all combinations
            if not combinations_:
                # Fully factorial experiment, shortcut for "combinations":[[],[]]
                combinations_sweeps = []
                combinations = [[]]
            else:
                # First item in combinations list is a list of sweeps
                combinations_sweeps = combinations_[0]
                # then - all combinations
                combinations = combinations_[1:]
            for item in combinations_sweeps:
                # TODO: error if sweep is already in this list?
                all_combinations_sweeps.append(item)
            all_combinations.append((combinations_sweeps, combinations))
        
        sweeps_fully_factorial = list(set(sweeps_all) - set(all_combinations_sweeps))
        #print "fully fact: %s" % sweeps_fully_factorial
        
        #2) produce a list of all combinations of fully factorial sweeps
        # First sets of "combinations": the fully-factorial sweeps
        for sweep in sweeps_fully_factorial:
            all_combinations.append(([sweep], [[x] for x in self.experiment["sweeps"][sweep].keys()]))
        
        #3) take the dot (inner) product of the list above (fully factorial arm combinations)
        #   with the first combinations list, that with the second combination list, ...
        # step-by-step reduce the list of combinations to a single item
        # (dot-product of each list of combinations)
        # this could use a lot of memory...
        red_iter = 0
        #print "all combinations:", red_iter, all_combinations
        while len(all_combinations) > 1:
            comb1 = all_combinations[0]
            comb2 = all_combinations[1]
            new_sweeps = comb1[0] + comb2[0]
            new_combinations = [x+y for x in comb1[1] for y in comb2[1]]
            all_combinations = [(new_sweeps, new_combinations)] + all_combinations[2:]
            red_iter += 1
            #print "all combinations:", red_iter, all_combinations
        
        #4) write out the document for each in (3), which should specify one arm for each
        #   sweep with no repetition of combinations
        sweep_names = all_combinations[0][0]
        combinations = all_combinations[0][1]
        for combination in combinations:
            scenario = Scenario(self._apply_combination(self.experiment["base"], sweep_names, combination))
            scenario.parameters = dict(zip(sweep_names, combination))

            if generate_seed:
                # Replace seed if requested by the user
                if "@seed@" in scenario.xml:
                    scenario.xml = scenario.xml.replace("@seed@", str(seed.next()))
                else:
                    raise(RuntimeError("@seed@ placeholder is not found"))
            yield scenario
    
    def add_sweep(self, sweep_name):
        self.experiment["sweeps"][sweep_name] = {}

    def add_arm(self, sweep, arm_name, parameters):
        self.experiment["sweeps"][sweep][arm_name] = parameters