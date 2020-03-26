from django.test import TestCase

from creatures.data import PROFICIENCY_DICT, PROFICIENCY_EXP
from creatures.utils import get_proficiency_verbose


class CreatureUtilsTestCase(TestCase):
    def test__get_proficiency_verbose__returns_correct_value(self):
        expected_value = PROFICIENCY_DICT.get(PROFICIENCY_EXP)
        value = get_proficiency_verbose(PROFICIENCY_EXP)
        self.assertEqual(value, expected_value)
