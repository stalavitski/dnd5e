import os
from pathlib import Path

from django.conf import settings
from django.test import TestCase

from characters.data import PROFICIENCY_EXP, PROFICIENCY_NONE, PROFICIENCY_PROF
from characters.models import CharacterDetails
from characters.utils import get_proficiency_by_priority, portrait_upload_to


class CharacterUtilsTestCase(TestCase):
    def _create_test_file(self, path):
        # Create path if it does not exist
        dir_path, _ = os.path.split(path)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Create a dummy file
        with open(path, 'w') as f:
            f.write('test')
            f.close()

    # get_proficiency_by_priority tests
    def test__get_proficiency_by_priority__returns_none__when_it_is_only_option(self):
        result = get_proficiency_by_priority(PROFICIENCY_NONE, PROFICIENCY_NONE, PROFICIENCY_NONE)
        self.assertEqual(result, PROFICIENCY_NONE)

    def test__get_proficiency_by_priority__returns_prof__when_it_is_passed_and_no_exp_passed(self):
        result = get_proficiency_by_priority(PROFICIENCY_NONE, PROFICIENCY_PROF, PROFICIENCY_NONE)
        self.assertEqual(result, PROFICIENCY_PROF)

    def test__get_proficiency_by_priority__returns_exp__if_it_is_passed(self):
        result = get_proficiency_by_priority(PROFICIENCY_EXP, PROFICIENCY_PROF, PROFICIENCY_NONE)
        self.assertEqual(result, PROFICIENCY_EXP)

    # portrait_upload_to tests
    def test__portrait_upload_to__returns_correct_path(self):
        character_details = CharacterDetails(id=0)
        file_name = '{}.png'.format(character_details.id)
        expected_result = os.path.join('character_details', 'portrait', str(character_details.id), file_name)
        upload_to = portrait_upload_to(character_details, 'test.png')
        self.assertEqual(upload_to, expected_result)

    def test__portrait_upload_to__removes_previous_file(self):
        character_details = CharacterDetails(id=0)
        file_name = '{}.png'.format(character_details.id)
        path = os.path.join(
            settings.MEDIA_ROOT, 'character_details', 'portrait', str(character_details.id), file_name)
        self._create_test_file(path)
        self.assertTrue(os.path.exists(path))
        portrait_upload_to(character_details, 'test.png')
        self.assertFalse(os.path.exists(path))
