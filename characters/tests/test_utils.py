import os
from pathlib import Path

from django.conf import settings
from django.test import TestCase

from characters.models import CharacterDetails
from characters.utils import portrait_upload_to


class CharacterUtilsTestCase(TestCase):
    def _create_test_file(self, path):
        # Create path if it does not exist
        dir_path, _ = os.path.split(path)
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Create a dummy file
        with open(path, 'w') as f:
            f.write('test')
            f.close()

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
