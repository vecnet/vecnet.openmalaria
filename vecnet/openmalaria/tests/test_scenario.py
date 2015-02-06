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
import copy

import unittest
import os

from vecnet.openmalaria.scenario import Scenario
from vecnet.openmalaria.scenario.entomology import Vector
from vecnet.openmalaria.scenario.monitoring import Monitoring

base_dir = os.path.dirname(os.path.abspath(__file__))


class TestGetSchemaVersion(unittest.TestCase):
    def setUp(self):
        pass

    def test_scenario(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))).read())
        # Reading attributes
        self.assertEqual(scenario.name, "Olyset Duo")
        self.assertEqual(scenario.schemaVersion, 32)
        self.assertRaises(AttributeError, getattr, scenario, "wuID")
        self.assertRaises(AttributeError, lambda: scenario.analysisNo)

        # Changing attributes
        scenario.name = "Test name"
        self.assertEqual(scenario.name, "Test name")
        self.assertRaises(AssertionError, setattr, scenario, "name", 1)
        self.assertRaises(AttributeError, setattr, scenario, "schemaVersion", 31)

        # Check if xml code is correct
        self.assertEqual(len(scenario.xml), 20613)

        # Changing attributes
        scenario.wuID = 1
        self.assertEqual(scenario.wuID, 1)
        self.assertRaises(AssertionError, setattr, scenario, "wuID", "string")

        scenario.analysisNo = 1024
        self.assertEqual(scenario.analysisNo, 1024)
        self.assertRaises(AssertionError, setattr, scenario, "analysisNo", "string")

        # Checking sections
        self.assertEqual(hasattr(scenario, "monitoring"), True)
        self.assertIsInstance(scenario.monitoring, Monitoring)

    def test_monitoring(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))).read())
        self.assertEqual(scenario.monitoring.name, "Monthly Surveys")
        self.assertEqual(scenario.monitoring.detectionLimit, 100.0)
        self.assertEqual(scenario.monitoring.surveys, [730, 736, 742, 748])
        self.assertEqual(len(scenario.monitoring.surveys), 4)
        self.assertEqual(scenario.monitoring.continuous, ['simulated EIR', 'GVI coverage'])
        measures = scenario.monitoring.continuous
        measures.append("Input EIR")
        scenario.monitoring.continuous = measures
        self.assertEqual(scenario.monitoring.continuous, ['simulated EIR', 'GVI coverage', 'Input EIR'])
        self.assertEqual(scenario.monitoring.SurveyOptions, ['nHost', 'nPatent', 'nUncomp', 'simulatedEIR', 'nMassGVI'])

    def test_entomology(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))).read())

        # Reading attributes
        self.assertEqual(scenario.entomology.name, "Kenya Lowlands from EMOD")
        self.assertEqual(scenario.entomology.scaledAnnualEIR, 25.0)
        self.assertEqual(len(scenario.entomology.vectors), 1)
        for vector in scenario.entomology.vectors:
            self.assertIsInstance(vector, Vector)
            self.assertEqual(vector.mosquito, "gambiae")
            self.assertEqual(vector.propInfected, 0.078)

        gambiae = scenario.entomology.vectors["gambiae"]
        self.assertIsInstance(gambiae, Vector)
        self.assertEqual(gambiae.mosquito, "gambiae")
        self.assertEqual(gambiae.seasonality.annualEIR, 1.0)
        self.assertEqual(gambiae.seasonality.input, "EIR")
        self.assertEqual(gambiae.seasonality.smoothing, "fourier")
        self.assertEqual(gambiae.seasonality.monthlyValues,
                         [0.0468, 0.0447, 0.0374, 0.0417, 0.0629, 0.0658, 0.0423, 0.0239, 0.0203, 0.0253, 0.0331, 0.0728])
        self.assertEqual(gambiae.mosq.minInfectedThreshold, 0.001)
        self.assertEqual(gambiae.mosq.mosqRestDuration, 2)
        self.assertEqual(gambiae.mosq.mosqHumanBloodIndex, 0.85)

        # Writing attributes
        gambiae.seasonality.monthlyValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertRaises(AssertionError, setattr, gambiae, "propInfected", "string")
        gambiae.propInfected = 0.1
        scenario.entomology.scaledAnnualEIR = 10.0
        gambiae.seasonality.annualEIR = 6.1
        gambiae.mosq.mosqHumanBloodIndex = 0.7

        scenario2 = Scenario(scenario.xml)
        self.assertEqual(scenario2.entomology.vectors["gambiae"].seasonality.monthlyValues,
                             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.assertEqual(scenario2.entomology.vectors["gambiae"].propInfected, 0.1)
        self.assertEqual(scenario2.entomology.vectors["gambiae"].seasonality.annualEIR, 6.1)
        self.assertEqual(scenario2.entomology.scaledAnnualEIR, 10.0)
        self.assertEqual(scenario2.entomology.vectors["gambiae"].mosq.mosqHumanBloodIndex, 0.70)

        # Deleting a mosquito
        scenario2.entomology.vectors["gambiae"].mosquito = "farauti"
        for vector in scenario2.entomology.vectors:
            self.assertEqual(vector.mosquito, "farauti")
        del scenario.entomology.vectors["gambiae"]
        scenario3 = Scenario(scenario.xml)
        self.assertEqual(len(scenario3.entomology.vectors), 0)
        self.assertRaises(AttributeError, scenario3.entomology.vectors.add, "<anopheles/>")
        for vector in scenario3.entomology.vectors:
            print vector

    def test_interventions(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))).read())
        self.assertEqual(scenario.interventions.changeHS, [])
        self.assertIs(scenario.interventions.changeEIR, None)
        print len(scenario.interventions.human)
        for intervention in scenario.interventions.human:
            print intervention
            print intervention.name
            print intervention.decay
            print intervention.decay.function

    @classmethod
    def not_a__full_scenario(cls):
        scenario = Scenario() # scenario70k60c.xml

        scenario.schemaVersion = 32

        scenario.name = "Olyset Due"

        scenario.demography.maximumAgeYrs = 90
        scenario.demography.name = "Ranchuonyo"
        scenario.demography.popSize = 1000
        scenario.demography.ageGroup.lowerbound = 0
        # It may be important to preserve the order of the age groups in demography section
        scenario.demography.ageGroup.group = [{"poppercent":2.5,"lowerbound":0,"upperbound":5},]

        scenario.monitoring.name = "Monthly Surveys"
        scenario.monitoring.detectionLimit = 100
        scenario.monitoring.continuous = ["simulated EIR", "GVI coverage"]
        scenario.monitoring.continuous.append("input EIR")
        scenario.monitoring.surveyOptions = ["hHost", "nPatent", "nUncomp", "simulatedEIR", "nMassGVI"]
        scenario.monitoring.surveys = [730, 736, ]
        # We must preserve the order of the age groups, in monitoring section (for parsing survey output files)
        scenario.monitoring.ageGroup = [0, 90]  # [0, 0.5 1, 5, 18, 90]

        scenario.entomology.name = "Kenya Lowlands from EMOD"
        scenario.entomology.mode = "dynamic"
        scenario.scaledAnnualEIR = 25
        scenario.entomology.vectors = []

        gambiae = Vector()
        gambiae.name = "gambiae"
        gambiae.propInfected = 0.078
        gambiae.propInfectious = 0.015
        gambiae.seasonality.annualEIR = 1
        gambiae.seasonality.input = "EIR"
        gambiae.seasonality.smoothing = "fourier"
        gambiae.seasonality.monthlyValues = [0.0468, 0.0447, 0.0374, 0.0417, 0.0629, 0.0658, 0.0423, 0.0239, 0.0203, 0.0253, 0.0331, 0.0728]
        gambiae.mosq.minIfectedThreshold = 0.001
        gambiae.mosq.extrinsicIncubationPeriod = 12
        gambiae.mosq.mosqLaidEggsSameDayProportion = 0.313
        gambiae.mosq.mosqSeekingDuration = 0.33
        gambiae.mosq.mosqSurvivalFeedingCycleProbability = 0.623
        gambiae.mosq.availabilityVariance = 0
        gambiae.mosq.mosqProbBiting.mean = 0.95
        gambiae.mosq.mosqProbBiting.variance = 0
        gambiae.mosq.mosqProbFindRestSite.mean = 0.95
        gambiae.mosq.mosqProbFindRestSite.variance = 0
        gambiae.mosq.mosqProbResting.mean = 0.99
        gambiae.mosq.mosqProbResting.variance = 0
        gambiae.mosq.mosqProbOvipositing = 0.88
        gambiae.mosq.mosqHumanBloodIndex = 0.85
        # scenario.entomology.vectors
        # List of vecnet.openmalaria.scenario.Vector classes (<vector> tag
        # Defines a list of mosquitoes and their parameters
        scenario.entomology.vectors.append(gambiae)
        scenario.entomology.nonHumanHosts.unprotectedAnimals.number = 1.0

        scenario.healthSystem.ImmediateOutcomes.name = "Kenya ACT"
        scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareUncomplicated1 = 0.04
        scenario.healthSystem.ImmediateOutcomes.pSelfTreatUncomplicated = 0.0212
        scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareUncomplicated2 = 0.04
        scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareSevere = 0.48
        scenario.healthSystem.ImmediateOutcomes.firstLine = "ACT"
        scenario.healthSystem.ImmediateOutcomes.secondLine = "QN"
        scenario.healthSystem.ImmediateOutcomes.inpatient = "QN"
        scenario.healthSystem.ImmediateOutcomes.drugs.selfTreatment.initialACR = 0.63
        scenario.healthSystem.ImmediateOutcomes.drugs.selfTreatment.compliance = 0.85
        scenario.healthSystem.ImmediateOutcomes.drugs.selfTreatment.nonCompliersEffective = 0
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.initialACT = 0.96
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.compliance = 0.96
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.nonCompliersEffective = 0.96
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.treatmentActions.name = "clear blood-stage infections"
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.treatmentActions.clearInfections.stage = "blood" # blood, liver or both
        scenario.healthSystem.ImmediateOutcomes.drugs.ACT.treatmentActions.clearInfections.timestep = 1
        # scenario.healthSystem.CFR - Case fatality rate for inpatients
        # scenario.healthSystem.CFR.interpolation = "none"
        scenario.healthSystem.CFR.group = [{"lowerbound": 0.0, "value": 0.0918900},
                                           {"lowerbound": 0.25, "value": 0.0810811},
                                           ]
        # Probabilities of sequelae (a condition that is the consequence of a previous disease or injury) in inpatients
        scenario.healthSystem.pSequelaeInpatient.interpolation = "none"
        scenario.healthSystem.pSequelaeInpatient.group = [{"lowerbound":0.0, "value":0.0132},
                                                          {"lowerbound":5.0, "value":"0.005"}
                                                          ]


        scenario.interventions.name = "Olyset"
        # scenario.interventions.changeHS.name = "123"
        # scenario.interventions.changeHS.time = 50
        # scenario.interventions.changeHS.healthSystem = ... # Define healthSystem

        # scenario.interventions.changeEIR.name = "123"
        # scenario.interventions.time = 45
        # scenario.interventions.EIRDaily = [1, 1.1, 1, 1.2, ... ]

        # scenario.interventions.importedInfections.name = "123
        # scenario.interventions.importedInfections.period = 0
        # scenario.interventions.importedIntections.timestamps = [1,2]

        scenario.interventions.human[0].type = "GVI"
        scenario.interventions.human[0].id = "GVI"
        scenario.interventions.human[0].name = "Nets"
        scenario.interventions.human[0].GVI.decay.function = "step"
        scenario.interventions.human[0].GVI.L = 50
        scenario.interventions.human[0].GVI.anophelesParams.gambiae.propActive = 0.7
        scenario.interventions.human[0].GVI.anophelesParams.gambiae.deterrency = 0.23076923077
        scenario.interventions.human[0].GVI.anophelesParams.gambiae.preprandialKillingEffect = 0.7
        scenario.interventions.human[0].GVI.anophelesParams.gambiae.postprandialKillingEffect  = 0
        scenario.interventions.human[0].deployment.timed = {730: {"coverage": 0.6},
                                                            736: {"coverage": 0.6}
                                                            # other keys may include maxAge, minAge, vaccMinPrevDoses etc
        }
        scenario.interventions.human[1].type = "ITN"


if __name__ == "__main__":
    unittest.main()
