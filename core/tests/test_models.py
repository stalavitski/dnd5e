from django.test import TestCase

from core.models import Dice


class DiceTestCase(TestCase):
    fixtures = ['0003_dices.json']

    def test__roll__returns_number_in_range(self):
        dice = Dice.objects.first()

        for i in range(1, 100):
            roll = dice.roll()
            # Roll should be in the range [1, num of the Dice sides]
            self.assertLessEqual(roll, dice.sides)
            self.assertGreaterEqual(roll, 1)
