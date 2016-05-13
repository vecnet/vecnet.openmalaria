# Copyright (C) 2016, University of Notre Dame
# All rights reserved
import unittest

from vecnet.openmalaria.scenario.interventions import Deployment


class TestScenario(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_timed(self):
        deployment = Deployment(None)
        deployment.create_from_xml("""
                <deployment name="Nets">
                <component id="LLIN" />
                <timed>
                    <deploy coverage="0.0" time="0" />
                    <deploy coverage="0.0" time="230" />
                    <deploy coverage="0.0" time="449" />
                </timed>
            </deployment>""")
        self.assertEqual(deployment.name, "Nets")
        self.assertEqual(len(deployment.components), 1)
        self.assertEqual(deployment.components[0], "LLIN")
        self.assertEqual(deployment.timesteps, [{"coverage": 0.0, "time": 0}, {'coverage': 0.0, 'time': 230}, {'coverage': 0.0, 'time': 449}])
        self.assertIsNone(deployment.continuous)

    def test_create_continuous(self):
        deployment = Deployment(None)
        deployment.create_from_xml("""
            <deployment>
                <component id="PEV" />
                <continuous>
                    <deploy coverage="0.0" targetAgeYrs="0.0833" />
                    <deploy coverage="0.0" targetAgeYrs="0.17" />
                    <deploy coverage="0.0" targetAgeYrs="0.25" />
                </continuous>
            </deployment>""")
        self.assertRaises(AttributeError, getattr, deployment, "name")
        self.assertEqual(len(deployment.components), 1)
        self.assertEqual(deployment.components[0], "PEV")
        self.assertRaises(AttributeError, getattr, deployment, "timesteps")
        self.assertEqual(deployment.continuous, [{'end': 2147483647, 'begin': 0, 'targetAgeYrs': 0.0833}, {'end': 2147483647, 'begin': 0, 'targetAgeYrs': 0.17}, {'end': 2147483647, 'begin': 0, 'targetAgeYrs': 0.25}])
