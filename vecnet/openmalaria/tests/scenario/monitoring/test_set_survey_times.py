import unittest

from vecnet.openmalaria.monitoring import set_survey_times


class SetSurveyTimesTest(unittest.TestCase):
    def test_monthly(self):
        result = set_survey_times(2000, 1, 2, 2011, "monthly")
        self.assertEqual(
            result,
            ['803', '809', '814', '821', '827', '833', '839', '845', '851', '857', '863', '869', '876', '882', '887']
        )

    def test_yearly(self):
        result = set_survey_times(2000, 5, 0, 2011, "yearly")
        self.assertEqual(
            result,
            ['803', '876', '949', '1022', '1095', '1168']
        )