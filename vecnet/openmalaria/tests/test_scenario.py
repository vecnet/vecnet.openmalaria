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


class TestScenario(unittest.TestCase):
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

    def test_healthsystem(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("input", "scenario70k60c.xml"))).read())

        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.name, "Kenya ACT")
        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareUncomplicated1, 0.04)
        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareUncomplicated2, 0.04)
        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.pSelfTreatUncomplicated, 0.0212)
        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.pSeekOfficialCareSevere, 0.48)
        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.firstLine, "ACT")

        scenario.healthSystem.ImmediateOutcomes.firstLine = "QN"

        self.assertEqual(scenario.healthSystem.ImmediateOutcomes.firstLine, "QN")

        self.assertEqual(len(scenario.healthSystem.ImmediateOutcomes.drugs), 3)

        for drug in scenario.healthSystem.ImmediateOutcomes.drugs:
            if drug.name == "ACT":
                self.assertEqual(drug.initialACR, 0.96)
                self.assertEqual(drug.compliance, 0.892)
                self.assertEqual(drug.nonCompliersEffective, 0.8544)
                self.assertEqual(drug.treatmentAction.name, 'clear blood-stage infections')
                self.assertEqual(drug.treatmentAction.timesteps, 1)
                self.assertEqual(drug.treatmentAction.stage, 'blood')

        scenario.healthSystem.ImmediateOutcomes.drugs.add("CQ", 0.5, ["initialACR", "compliance"])
        self.assertEqual(len(scenario.healthSystem.ImmediateOutcomes.drugs), 4)

        drug = scenario.healthSystem.ImmediateOutcomes.drugs["CQ"]
        self.assertEqual(drug.initialACR, 0.5)
        self.assertEqual(drug.compliance, 0.5)
        self.assertEqual(drug.treatmentAction, None)

        drug.treatmentAction = 'test'
        drug.treatmentAction.timesteps = 1
        drug.treatmentAction.stage = 'blood'

        self.assertEqual(drug.treatmentAction.name, 'test')
        self.assertEqual(drug.treatmentAction.timesteps, 1)
        self.assertEqual(drug.treatmentAction.stage, 'blood')


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
                         [0.0468, 0.0447, 0.0374, 0.0417, 0.0629, 0.0658, 0.0423, 0.0239, 0.0203, 0.0253, 0.0331,
                          0.0728])
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
        for intervention in scenario.interventions.human:
            self.assertEqual(intervention.name, "Nets")
            self.assertEqual(intervention.decay.function, "step")
            self.assertEqual(len(intervention.anophelesParams), 1)
            self.assertEqual(intervention.anophelesParams[0].mosquito, "gambiae")
            self.assertEqual(intervention.anophelesParams[0].propActive, 0.7)
            self.assertEqual(intervention.anophelesParams[0].deterrency, 0.23076923077)
            self.assertEqual(intervention.anophelesParams[0].preprandialKillingEffect, 0.7)
            self.assertEqual(intervention.anophelesParams[0].postprandialKillingEffect, 0)

            intervention.anophelesParams[0].postprandialKillingEffect = 0.2
            self.assertEqual(intervention.anophelesParams[0].postprandialKillingEffect, 0.2)

            new_anopheles_params = {
                "mosquito": "gambiae",
                "propActive": 0.8,
                "deterrency": 0.2222,
                "preprandialKillingEffect": 0.9,
                "postprandialKillingEffect": 0.1
            }
            intervention.add_or_update_anophelesParams(new_anopheles_params)

            self.assertEqual(intervention.anophelesParams[0].mosquito, "gambiae")
            self.assertEqual(intervention.anophelesParams[0].propActive, 0.8)
            self.assertEqual(intervention.anophelesParams[0].deterrency, 0.2222)
            self.assertEqual(intervention.anophelesParams[0].preprandialKillingEffect, 0.9)
            self.assertEqual(intervention.anophelesParams[0].postprandialKillingEffect, 0.1)

            # Overwrite anophelesParams.
            anopheles_xml = """<anophelesParams mosquito="funestus" propActive="0.0">
                                <deterrency value="0.0" />
                                <preprandialKillingEffect value="0.0" />
                                <postprandialKillingEffect value="0.0" />
                               </anophelesParams>"""
            intervention.anophelesParams = [anopheles_xml]

            self.assertEqual(len(intervention.anophelesParams), 1)
            self.assertEqual(intervention.anophelesParams[0].mosquito, "funestus")
            self.assertEqual(intervention.anophelesParams[0].propActive, 0.0)
            self.assertEqual(intervention.anophelesParams[0].deterrency, 0.0)
            self.assertEqual(intervention.anophelesParams[0].preprandialKillingEffect, 0.0)
            self.assertEqual(intervention.anophelesParams[0].postprandialKillingEffect, 0)

        component_xml = """<component id="DDT" name="DDT">
                             <GVI>
                               <decay L="0.5" function="exponential"/>
                             </GVI>
                           </component>"""

        self.assertEqual(len(scenario.interventions.human), 1)
        scenario.interventions.human.add(component_xml)
        self.assertEqual(len(scenario.interventions.human), 2)

        scenario.interventions.human.add(component_xml, "testing")
        self.assertEqual(len(scenario.interventions.human), 3)
        self.assertTrue(scenario.interventions.human["testing"] is not None)
        self.assertEqual(scenario.interventions.human["testing"].id, "testing")

        ddt = scenario.interventions.human["DDT"]
        self.assertEqual(ddt.id, "DDT")
        self.assertEqual(ddt.name, "DDT")
        self.assertEqual(ddt.decay.L, 0.5)
        self.assertEqual(ddt.decay.function, "exponential")

        mda_xml = """
                    <component id="Coartem" name="Coartem">
                        <MDA>
                            <effects>
                                <option name="0.5" pSelection="0.5">
                                    <clearInfections stage="liver" timesteps="1"/>
                                    <clearInfections stage="blood" timesteps="3"/>
                                </option>
                                <option name="0.2" pSelection="0.2">
                                    <clearInfections stage="liver" timesteps="1"/>
                                    <clearInfections stage="blood" timesteps="4"/>
                                </option>
                                <option name="0.3" pSelection="0.3">
                                    <clearInfections stage="liver" timesteps="1"/>
                                    <clearInfections stage="blood" timesteps="5"/>
                                </option>
                            </effects>
                        </MDA>
                    </component>
                    """

        scenario.interventions.human.add(mda_xml)
        self.assertEqual(len(scenario.interventions.human), 4)

        mda = scenario.interventions.human["Coartem"]
        self.assertEqual(mda.id, "Coartem")
        self.assertEqual(mda.name, "Coartem")
        self.assertEqual(len(mda.treatment_options), 3)
        self.assertEqual(mda.treatment_options[0]["name"], "0.5")

        mda_params = {
                "name": "0.5",
                "pSelection": "0.5",
                "deploys": [{
                    "maxAge": "10",
                    "minAge": "0",
                    "p": "1",
                    "components": ["Coartem"]
                }],
                "clearInfections": [{
                    "timesteps": "2",
                    "stage": "liver"
                }, {
                    "timesteps": "3",
                    "stage": "blood"
                }]
        }
        mda.add_or_update_treatment_option(mda_params)
        self.assertEqual(len(mda.treatment_options), 3)
        self.assertEqual(mda.treatment_options[0]["name"], "0.5")
        self.assertEqual(mda.treatment_options[0]["deploys"][0].p, 1)

        # Test deployment section
        self.assertEqual(len(scenario.interventions.human.deployments), 1)
        for deployment in scenario.interventions.human.deployments:
            self.assertEqual(deployment.name, "Nets")
            self.assertEqual(deployment.id, "GVI")
            self.assertEqual(len(deployment.timesteps), 185)
            self.assertEqual(deployment.timesteps[0]["coverage"], 0.6)
            self.assertEqual(deployment.timesteps[0]["time"], 730)

            # print deployment.timesteps
            # for timestep in deployment.timesteps:
            # print timestep["time"], timestep["coverage"]

        vector_pop_xml = """<intervention name="Larviciding">
                              <description>
                                <anopheles mosquito="gambiae">
                                  <emergenceReduction initial="0.8">
                                    <decay L="0.2465753424657534" function="step" />
                                  </emergenceReduction>
                                </anopheles>
                              </description>
                            </intervention>"""

        if len(scenario.interventions.vectorPop) == 0:
            scenario.interventions.add_section("vectorPop")

        scenario.interventions.vectorPop.add(vector_pop_xml)
        self.assertEqual(len(scenario.interventions.vectorPop), 1)

        for intervention in scenario.interventions.vectorPop:
            self.assertEqual(intervention.name, "Larviciding")

            self.assertEqual(len(intervention.anopheles), 1)
            for anopheles in intervention.anopheles:
                self.assertEqual(anopheles.mosquito, "gambiae")
                self.assertEqual(anopheles.emergenceReduction, 0.8)

                decay = anopheles.decays["emergenceReduction"]
                self.assertEqual(decay.L, 0.2465753424657534)
                self.assertEqual(decay.function, "step")

                anopheles.mosquito = "test"
                self.assertEqual(anopheles.mosquito, "test")
                anopheles.emergenceReduction = 0.3
                self.assertEqual(anopheles.emergenceReduction, 0.3)

            new_anopheles = {
                "mosquito": "test",
                "emergenceReduction": 0.9
            }
            intervention.add_or_update_anopheles(new_anopheles)

            self.assertEqual(intervention.anopheles[0].mosquito, "test")
            self.assertEqual(intervention.anopheles[0].emergenceReduction, 0.9)

        scenario.interventions.vectorPop.add(vector_pop_xml, "test")
        self.assertEqual(len(scenario.interventions.vectorPop), 2)
        self.assertTrue(scenario.interventions.vectorPop["test"] is not None)
        self.assertEqual(scenario.interventions.vectorPop["test"].name, "test")

        # Scenario without interventions
        scenario1 = Scenario(
            open(os.path.join(base_dir, os.path.join("input", "scenario70k60c_no_interventions.xml"))).read())
        self.assertEqual(len(scenario1.interventions.human.deployments), 0)
        i = 0
        for deployment in scenario1.interventions.human.deployments:
            i += 1
        self.assertEqual(i, 0)
        self.assertRaises(KeyError, lambda x: scenario1.interventions.human["123"], 1)
        i = 0
        self.assertEqual(len(scenario1.interventions.human), 0)
        for intervention in scenario1.interventions.human:
            i += 1
        self.assertEqual(i, 0)

        # Scenario without deployments in intervention section
        scenario1 = Scenario(
            open(os.path.join(base_dir, os.path.join("input", "scenario70k60c_no_deployments.xml"))).read())
        self.assertEqual(len(scenario1.interventions.human.deployments), 0)
        i = 0
        for deployment in scenario1.interventions.human.deployments:
            i += 1
        self.assertEqual(i, 0)
        # self.assertRaises(KeyError, lambda x: scenario1.interventions.deployments["123"], 1)

    def test_vectorpop_intervention(self):
        # No vectorPop section
        scenario = Scenario(
            open(os.path.join(base_dir, os.path.join("input", "scenario70k60c_no_interventions.xml"))).read())
        self.assertEqual(scenario.interventions.vectorPop.interventions, {})
        self.assertEqual(len(scenario.interventions.vectorPop), 0)
        i = None
        for i in scenario.interventions.vectorPop:
            print i.name
        self.assertIsNone(i)  # make sure iterator returns an empty set

        # Empty vectorPop section
        scenario = Scenario(
            open(os.path.join(base_dir, os.path.join("files", "test_scenario", "empty_vectorpop_section.xml"))).read())
        self.assertEqual(scenario.interventions.vectorPop.interventions, {})
        self.assertEqual(len(scenario.interventions.vectorPop), 0)
        i = None
        for i in scenario.interventions.vectorPop:
            print i.name
        self.assertIsNone(i)  # make sure iterator returns an empty set

        # Test vectorPop section with exactly one intervention
        scenario = Scenario(
            open(os.path.join(base_dir, os.path.join("files", "test_scenario", "larvacing.xml"))).read())
        self.assertEqual(len(scenario.interventions.vectorPop), 1)
        for i in scenario.interventions.vectorPop:
            self.assertEqual(i.name, "simple larviciding translated from schema 30")

        # Test vectorPop section with multiple interventions
        scenario = Scenario(
            open(os.path.join(base_dir, os.path.join("files", "test_scenario", "triple_larvacing.xml"))).read())
        self.assertEqual(len(scenario.interventions.vectorPop), 3)
        self.assertEqual(scenario.interventions.vectorPop["int1"].name, "int1")
        self.assertEqual(scenario.interventions.vectorPop["int2"].name, "int2")
        self.assertEqual(scenario.interventions.vectorPop["int3"].name, "int3")
        self.assertRaises(KeyError, lambda: scenario.interventions.vectorPop["int4"])

        # test name setter
        scenario.interventions.vectorPop["int1"].name = "new name"
        self.assertEqual(scenario.interventions.vectorPop["new name"].name, "new name")

    def test_vaccine_interventions(self):
        scenario = Scenario(open(os.path.join(base_dir, os.path.join("files", "test_scenario", "vaccine_interventions.xml"))).read())

        self.assertEqual(len(scenario.interventions.human), 2)

        for i in scenario.interventions.human:
            if i.vaccine_type == "TBV":
                tbv = i
            else:
                pev = i

        self.assertEqual(tbv.id, "my_TBV_effect")
        self.assertEqual(pev.id, "some_PEV")
        self.assertEqual(tbv.efficacyB, 10)
        self.assertEqual(pev.efficacyB, 10)
        self.assertEqual(tbv.initialEfficacy, [0.512, 0.64, 0.8])
        self.assertEqual(pev.initialEfficacy, [0.512, 0.64, 0.8])

        self.assertEqual(len(scenario.interventions.human.deployments), 1)

        continuous = None
        timed = None
        for d in scenario.interventions.human.deployments:
            continuous = d.continuous
            timed = d.timesteps

        self.assertEqual(len(continuous), 3)
        self.assertEqual(len(timed), 6)

        self.assertEqual(continuous[0]["targetAgeYrs"], 0.0833)
        self.assertEqual(timed[0]["time"], 1)
        self.assertEqual(timed[0]["coverage"], 0.95)

if __name__ == "__main__":
    unittest.main()
