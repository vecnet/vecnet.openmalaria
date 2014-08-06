#!/bin/env python2
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of
# the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import itertools
import re

class ExperimentDescription:
    """
    OpenMalaria experiment description is a json file. This class is an SDK for working with that file format.
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

    def __str__(self):
        return self.name

    def _product(self, sweeps):
        if len(sweeps) == 0:
            return None
        lst = []
        for sweep in sweeps:
            lst.append(self.experiment["sweeps"][sweep].keys())
        product = itertools.product(*lst)
        return product

    def _apply_changes(self, scenario, sweep_name, arm_name):
        arm = self.experiment["sweeps"][sweep_name][arm_name]
        for param_change in arm:
            # arm substitution string should start and end with an @
            if re.match("^@.*@$",param_change) is None:
                raise TypeError("arm substitution string should start and end with an @, for example @param1@")
            # Each arm may contain more that one parameter
            # changes are applied in a random order currently
            param_value = arm[param_change]
            if isinstance(param_value, (int, float)):
                param_value = str(param_value)
            scenario = scenario.replace(param_change, param_value)
        return scenario

    def _apply_combination(self, scenario, sweeps_applied, combination):
        for i in range(0, len(sweeps_applied)):
        # Apply sweeps in order defined by user
            sweep = sweeps_applied[i]
            arm = combination[i]
            scenario = self._apply_changes(scenario, sweep, arm)
        return scenario

    def _scenarios(self, product, sweeps_in_this_combination):
        new_combination_list = product
        new_product = self._product(sweeps_in_this_combination)
        if new_product is not None:
            new_product = list(new_product)
        else:
            return product
        if product == []:
            if new_product is not None:
                return new_product
            else:
                return product
        if new_product is not None:
            new_combination_list = []
            for item in itertools.product(product, new_product):
                new_combination_list.append(list(itertools.chain(*item)))
        return new_combination_list


    def scenarios(self):
        """
        Generator function. Spits out scenarios for this experiment
        """
        sweeps_all = self.experiment["sweeps"].keys()
        if isinstance(self.experiment["combinations"], list):
            # For backward compatibility with experiments1-4s
            combinations_in_experiment = {" ": self.experiment["combinations"]}
            #if self.experiment["combinations"] == []:
            #    # Special notation for fully-factorial experiments
            #    combinations_in_experiment = {" ":[[],[]]}
        else:
            # Combinations must be a dictionary in this particular case
            combinations_in_experiment = self.experiment["combinations"]


        #TODO: this needs to be done in multiple steps:
        #1) calculate sweeps_non_fully_factorial (depends on ALL combinations_ items)
        #2) produce a list of all combinations of fully factorial sweeps
        #3) take the dot (inner) product of the list above (fully factorial arm combinations)
        #   with the first combinations list, that with the second combination list, ...
        #4) write out the document for each in (3), which should specify one arm for each
        #   sweep with no repetition of combinations
        #Note: most of (3) could be done in step (1), avoiding the need to iterate over the lists of combinations twice

        # Get the list of fully factorial sweeps
        all_sweeps_non_fully_factorial = []
        for key, combinations_ in combinations_in_experiment.items():
            # generate all permutations of all combinations
            if combinations_ == []:
                # Fully factorial experiment, shortcut for "combinations":[[],[]]
                sweeps_non_fully_factorial = []
                combinations = [[]]
            else:
                # First item in combinations list is a list of sweeps\
                sweeps_non_fully_factorial = combinations_[0]
                # then - all combinations
                combinations = combinations_[1:]
            for item in sweeps_non_fully_factorial:
                all_sweeps_non_fully_factorial.append(item)
        sweeps_fully_factorial = list(set(sweeps_all) - set(all_sweeps_non_fully_factorial))
        print "fully fact: %s" % sweeps_fully_factorial

        product = []
        for key, combinations_ in combinations_in_experiment.items():
            # generate all permutations of all combinations
            if combinations_ == []:
                # Fully factorial experiment, shortcut for "combinations":[[],[]]
                sweeps_non_fully_factorial = []
                combinations = [[]]
            else:
                # First item in combinations list is a list of sweeps\
                sweeps_non_fully_factorial = combinations_[0]
                # then - all combinations
                combinations = combinations_[1:]
            product = self._scenarios(product, sweeps_non_fully_factorial)
            #product = list(product)
            print product

        # Generate cartesian product of fully factorial sweeps + non fully factorial sweeps
        pass
        #print product

        for key, combinations_ in combinations_in_experiment.items():
            if combinations_ == []:
                # Fully factorial experiment, shortcut for "combinations":[[],[]]
                sweeps_non_fully_factorial = []
                combinations = [[]]
            else:
                # First item in combinations list is a list of sweeps\
                sweeps_non_fully_factorial = combinations_[0]
                # then - all combinations
                combinations = combinations_[1:]

            sweeps_fully_factorial = list(set(sweeps_all)-set(sweeps_non_fully_factorial))

            for combination in combinations:
                scenario = self._apply_combination(self.experiment["base"], sweeps_non_fully_factorial, combination)
                product = self._product(sweeps_fully_factorial)
                if product is not None:
                    # Apply fully factorial sweeps
                    for combination1 in product:
                        yield self._apply_combination(scenario, sweeps_fully_factorial, combination1)
                else:
                    yield scenario

    def add_sweep(self, sweep_name):
       self.experiment["sweeps"][sweep_name] = {}

    def add_arm(self, sweep, arm_name, parameters):
        self.experiment["sweeps"][sweep][arm_name] = parameters

if __name__ == "__main__":
    print "use \"python test.py\" to run unittest"
    pass