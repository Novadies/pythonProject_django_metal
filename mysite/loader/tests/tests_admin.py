from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from unittest.mock import MagicMock

from loader.admin import Upload
from loader.models import UploadFiles


class ModelTestCaseA(TestCase):
    @classmethod
    def tearDownClass(cls):
        """ удаление директории тест юзер. В директорию записываются file1 и file2.
        Директория может удалиться только при отсутствии файлов. Соответственно это тестирует удаляемость файлов
        """
        uploads_directory = settings.MEDIA_ROOT.joinpath('uploads').joinpath('test_user')
        print(f'Создана временная директория: {uploads_directory}, '
              f'она сразу же удаляется и не видна. Что бы её увидеть требуется закоментировать tearDownClass')
        uploads_directory.rmdir()

    def setUp(self):
        self.model = UploadFiles
        self.user = get_user_model().objects.create(username='test_user')
        # Создаем временные файлы для тестов
        file_content1 = b'Content of file 1'
        file_content2 = b'Content of file 2'
        # Сохраняем временные файлы
        file1 = SimpleUploadedFile('file1.txt', file_content1)
        file2 = SimpleUploadedFile('file2.txt', file_content2)
        # Создаем объекты модели с указанием временных файлов
        self.count = self.model.objects.count()
        self.obj1 = self.model.objects.create(file_to_upload=file1, to_user=self.user)
        self.obj2 = self.model.objects.create(file_to_upload=file2, to_user=self.user)
        self.queryset = self.model.objects.all()

    def test_delete_queryset(self):
        """ создаём и удаляем файл """
        self.request = MagicMock()
        count = self.count + 2   # так как создаём 2 записи
        self.assertEqual(self.model.objects.count(), count)
        # Запускаем метод delete_queryset
        Upload(model=UploadFiles, admin_site=None).delete_queryset(self.request, self.queryset)
        self.assertEqual(self.model.objects.count(), self.count)



