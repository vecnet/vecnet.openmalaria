__author__ = 'Alexander'

import json
import itertools
import sys
import re


class ExperimentDescription:
    """
    OpenMalaria experiment description is a json file. This class is an SDK for working with that file format.
    """
    def __init__(self, experiment):
        # Accept both json string and dictionary as an input. string is converted to dict automatically
        if isinstance(experiment, str):
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
                raise RuntimeError("arm substitution string should start and end with an @, for example @@param1@@")
            # Each arm may contain more that one parameter
            # changes are applied in a random order
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

    def scenarios(self):
        """
        Generator function. Spits out scenarios for this experiment
        """
        sweeps_all = self.experiment["sweeps"].keys()
        if isinstance(self.experiment["combinations"], list):
            # For backward compatibility with experiments1-4s
            # First item in combinations list is a list of sweeps, then - all combinations
            sweeps_non_fully_factorial = self.experiment["combinations"][0]
            combinations = self.experiment["combinations"][1:]

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
        else:
            for key, combinations_ in self.experiment["combinations"].items():
                sweeps_non_fully_factorial = combinations_[0]
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

def run_tests():
    experiment = {}
    experiment["base"] = "<xml>@itn@ @irs@ </xml>"
    experiment["sweeps"] = {}
    experiment["sweeps"]["itn"] = {"itn 80":{"@itn@":"80"},"itn 90":{"@itn@":"90"}}
    experiment["sweeps"]["irs"] = {"irs 66":{"@irs@":"66"},"irs 90":{"@irs@":"90"}}
    experiment["combinations"] = [
["itn","irs"],
["itn 80", "irs 66"],
["itn 80", "irs 90"],
["itn 90", "irs 66"]
]

    exp = ExperimentDescription(experiment)
    print exp
    for scenario in exp.scenarios():
        print scenario

    print "experiment1.json"
    fp = open("experiment1.json", "r")
    exp=ExperimentDescription(json.load(fp))
    for scenario in exp.scenarios():
        print scenario

    print "experiment2.json"
    with open("experiment2.json", "r") as fp:
        exp=ExperimentDescription(fp)
    for scenario in exp.scenarios():
        print scenario

    print "experiment3.json"
    with open("experiment3.json", "r") as fp:
        exp=ExperimentDescription(fp)
    for scenario in exp.scenarios():
        print scenario

    print "experiment4.json"
    with open("experiment4.json", "r") as fp:
        exp=ExperimentDescription(fp)
    try:
        for scenario in exp.scenarios():
            print scenario
    except RuntimeError:
        print "[PASS] Runtime Error raised as expected."
    else:
        print "[FAILED] Not RuntimeError exception raised"

    print "experiment5.json"
    with open("experiment5.json", "r") as fp:
        exp=ExperimentDescription(fp)
    for scenario in exp.scenarios():
        print scenario

    # Testing add_sweeps and add_arms functions
    print "experiment1.json modified"
    fp = open("experiment1.json", "r")
    exp=ExperimentDescription(json.load(fp))
    exp.experiment["base"] = "<xml> @itn@ @irs@ @model@ @p1@ (@p2@) </xml>"
    exp.add_sweep("test")
    exp.add_arm("test", "1", {"@p1@":2, "@p2@":"1"})
    exp.add_arm("test", "2", {"@p1@":1, "@p2@":"hey"})

    for scenario in exp.scenarios():
        print scenario


if __name__ == "__main__":
    if sys.argv[1] == "--test":
        run_tests()
        exit()
    pass