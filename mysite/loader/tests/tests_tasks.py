from unittest.mock import MagicMock
from django.test import TestCase
from loader.tasks import entry_to_db_task_Class_version


class TestCaseT(TestCase):
    def test_entry_to_db_task_Class_version(self):
        """ без понятия для чего этот тест, в целом имхо функция не нуждается в тесте """
        upload_instance = MagicMock()
        file_path = MagicMock()
        instance_DB_ExcelEntry = MagicMock()

        # Вызываем функцию entry_to_db_task_Class_version
        entry_to_db_task_Class_version(upload_instance, file_path, instance_DB_ExcelEntry)

        # Проверяем, что set_args был вызван с правильными аргументами
        instance_DB_ExcelEntry.set_args.assert_called_once_with(upload_instance=upload_instance, file_path=file_path)

        # Проверяем, что read_excel__to_dict был вызван
        instance_DB_ExcelEntry.read_excel__to_dict.assert_called_once()

        # Проверяем, что router был вызван с результатом read_excel__to_dict
        instance_DB_ExcelEntry.router.assert_called_once_with(instance_DB_ExcelEntry.read_excel__to_dict.return_value)

        # Проверяем, что entry_to_db был вызван с результатом router
        instance_DB_ExcelEntry.entry_to_db.assert_called_once_with(instance_DB_ExcelEntry.router.return_value)

