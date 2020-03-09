from django.test import TestCase

from core.data import ABILITY_CHARISMA, ABILITY_DICT
from core.utils import get_ability_name


class CoreUtilsTestCase(TestCase):
    def test__get_ability_name__returns_correct_value(self):
        expected_result = ABILITY_DICT.get(ABILITY_CHARISMA)
        self.assertEqual(get_ability_name(ABILITY_CHARISMA), expected_result)
