from unittest.mock import MagicMock, patch
from django.test import TestCase
from tenacity import RetryError

from loader.tools.logic import save_file


class TestCaseL(TestCase):
    def test_save_file__with_missing_file(self):
        self.model = MagicMock()
        self.request = MagicMock()
        uploaded_files = MagicMock()
        upload_instance = MagicMock()
        upload_instance.save.side_effect = Exception    # Вызываем исключение при сохранении
        with self.assertRaises(RetryError):             # Если применяется @retry обязательно оборачиваем в этот with
            with self.assertRaises(FileNotFoundError):    # Проверка на вызов исключения FileNotFoundError
                save_file(self, uploaded_files)

    # def test_something(self):
    #     response = self.client.get(reverse('some_app:files'))
    #     print(reverse('some_app:files'))
    #     self.assertEqual(200, response.status_code)
