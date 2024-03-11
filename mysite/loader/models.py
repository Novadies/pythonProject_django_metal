from pathlib import Path
from typing import Type, Any, Tuple

from model_utils import Choices
from model_utils.fields import StatusField
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from django.conf import settings
from django.db import models

from loader.validators import Item, Item1

_testmodel = ["numberlist", "id_fabrics", "id_work", "id_insta", "id_contract", "id_execut", "id_object", "id_cat",
              "id_med", ]

_testmodel1 = ["rectangular", "flanconnect", "flanthick", "dismantling", "mounting", "gostansi", ]


class TestModel(models.Model):
    for _i in _testmodel:
        locals()[_i] = models.CharField(
            max_length=99, blank=True)

    to_uploader = models.ForeignKey(
        "UploadFiles",
        on_delete=models.SET_NULL,
        related_name="testmodel",
        null=True,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="testmodel",
        null=True,
    )


class TestModel1(models.Model):
    for _i in _testmodel1:
        locals()[_i] = models.CharField(
            max_length=99, blank=True)

    to_uploader = models.ForeignKey(
        "UploadFiles",
        on_delete=models.SET_NULL,
        related_name="testmodel1",
        null=True,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="testmodel1",
        null=True,
    )


MODEL_VALIDATOR = ((TestModel, Item),
                   (TestModel1, Item1))


##############################################################################
# Это используется для тестов
@dataclass
class Aggregator:
    """ Агрегатор классов для записи в бд. Кортеж, содержащий кортежи из пар джанго-модель
     и соответствующий валидатор из пайдентик """
    mytuple: Tuple[Tuple[Type[models.Model], Type[BaseModel]], ...]


aggregator = Aggregator(MODEL_VALIDATOR)

##############################################################################

def user_directory_path(instance, filename):
    return Path('uploads') / instance.to_user.username / filename


class UploadFiles(models.Model):
    STATUS = Choices(('draft', 'НЕ ЗАПИСАНО В БД'), ('published', 'данные в базе'))
    db_record = StatusField()
    file_to_upload = models.FileField(upload_to=user_directory_path, null=True)
    time = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="upload_files",
        null=True,
    )
