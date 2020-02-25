from django.test import Client, TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Ability, Dice, Skill


class AbilityViewSetTestCase(TestCase):
    fixtures = ('0001_abilities.json',)

    def test__method_delete_is_not_allowed(self):
        ability = Ability.objects.first()
        client = Client()
        delete = client.post(reverse('ability-detail', (ability.id,)))
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__method_post_is_not_allowed(self):
        client = Client()
        post = client.post(reverse('ability-list'))
        self.assertEqual(post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class DiceViewSetTestCase(TestCase):
    fixtures = ('0003_dices.json',)

    def test__method_delete_is_not_allowed(self):
        dice = Dice.objects.first()
        client = Client()
        delete = client.post(reverse('dice-detail', (dice.id,)))
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__method_post_is_not_allowed(self):
        client = Client()
        post = client.post(reverse('dice-list'))
        self.assertEqual(post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SkillViewSetTestCase(TestCase):
    fixtures = ('0001_abilities.json', '0002_skills.json')

    def test__method_delete_is_not_allowed(self):
        skill = Skill.objects.first()
        client = Client()
        delete = client.post(reverse('skill-detail', (skill.id,)))
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test__method_post_is_not_allowed(self):
        client = Client()
        post = client.post(reverse('skill-list'))
        self.assertEqual(post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
