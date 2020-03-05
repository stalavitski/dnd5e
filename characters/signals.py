from django.db import models
from django.dispatch import receiver

from characters.models import Character, CharacterDetails
from core.data import ABILITY_DICT
from core.models import Skill


@receiver(models.signals.post_save, sender=Character)
def execute_after_save(sender, instance, created, *args, **kwargs):
    if created:
        # Create default abilities and saving throws
        for ability in ABILITY_DICT.keys():
            instance.character_abilities.create(ability=ability)
            instance.character_saving_throws.create(ability=ability)
        # Create default skills
        skill_ids = Skill.objects.values_list('id', flat=True)
        for skill_id in skill_ids:
            instance.character_skills.create(skill_id=skill_id)
        # Create a character details relation
        CharacterDetails.objects.create(character=instance, player_id=1)
