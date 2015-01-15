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

import unittest
import os

from vecnet.openmalaria.scenario import Scenario
from vecnet.openmalaria.scenario.monitoring import Monitoring


class TestGetSchemaVersion(unittest.TestCase):
    def setUp(self):
        pass

    def test_scenario(self):
        scenario = Scenario(open("input\\scenario70k60c.xml").read())
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
        self.assertEqual(len(scenario.xml), 20612)

        # Checking sections
        self.assertEqual(hasattr(scenario, "monitoring"), True)
        self.assertIsInstance(scenario.monitoring, Monitoring)


    def test_demography(self):
        pass


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