from contextlib import suppress
from io import BytesIO
from random import uniform
from typing import Generator, Literal, Type, Union

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from faker import Faker
import pytest
from unittest.mock import MagicMock
from django.db import models, connection
from django.conf import settings
from openpyxl.workbook import Workbook
from pydantic import ValidationError

from loader.models import aggregator, UploadFiles
from loader.tools.save_to_db_class import DB_ExcelEntry
from loader.validators import Item, Item1


# pytest C:\Users\RysukAO\PycharmProjects\intra\intra_services\loader\tests\tests_save_to_db_class_pytest.py -s

@pytest.fixture
def db_excel_entry():
    inst = DB_ExcelEntry(aggregator=aggregator)
    return inst

@pytest.fixture
def test_excel_file(tmp_path):
    # Создание временного файла Excel
    nf = "test_data.xlsx"
    file_path = tmp_path / nf
    with suppress(FileNotFoundError):    file_path.unlink()
    # Создание и заполнение Excel файла
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Name"
    sheet["B1"] = "Age"
    sheet["C1"] = "Occupation"
    # Данные для заполнения
    data = [
        ("Alice", 30, "Engineer"),
        ("Bob", 25, "Doctor"),
        ("Charlie", 35, "Teacher"),
        ("David", 40, "Artist"),
        ("Eve", 28, "Programmer")
    ]
    # Заполняем таблицу данными
    for row_index, (name, age, occupation) in enumerate(data, start=2):
        sheet[f"A{row_index}"] = name
        sheet[f"B{row_index}"] = age
        sheet[f"C{row_index}"] = occupation
    workbook.save(file_path)
    yield file_path         # Передаем путь к файлу как результат фикстуры
    file_path.unlink()      # После завершения теста удаляем временный файл

@pytest.fixture
def generate_random_data():
    """ Генерация данных учитывая валидацию [Item, Item1]
    Нужно следить за тем что генерируется, иначе будут ошибки
    """
    n = 5
    fake = Faker()
    return (
        {
            field_name: (
                int(uniform(1.0, 100.0)) if int in field_type.__args__ else
                uniform(1.0, 100.0) if float in field_type.__args__ else
                fake.name() if str in field_type.__args__ else
                "" if field_type is Literal[""] else None)
            for model in [Item, Item1] for field_name, field_type in model.__annotations__.items()
        }
        for _ in range(n)
    )

@pytest.fixture
def mock_model_fields():
    class MockModelField:
        def __init__(self, name, one_to_one=False, many_to_many=False, many_to_one=False, one_to_many=False):
            self.name = name
            self.one_to_one = one_to_one
            self.many_to_many = many_to_many
            self.many_to_one = many_to_one
            self.one_to_many = one_to_many
    field1 = MockModelField("field1", one_to_one=False, many_to_many=False, many_to_one=False, one_to_many=False)
    field6 = MockModelField("id", one_to_one=False, many_to_many=False, many_to_one=False, one_to_many=False)
    field2 = MockModelField("field2", one_to_one=True, many_to_many=False, many_to_one=False, one_to_many=False)
    field3 = MockModelField("field3", one_to_one=False, many_to_many=True, many_to_one=False, one_to_many=False)
    field4 = MockModelField("field4", one_to_one=False, many_to_many=False, many_to_one=True, one_to_many=False)
    field5 = MockModelField("field5", one_to_one=False, many_to_many=False, many_to_one=False, one_to_many=True)
    return [field1, field2, field3, field4, field5, field6]

########################################################################################################################
def test_set_args(db_excel_entry):
    upload_instance = "some_upload_instance"
    file_path = "some_file_path"
    db_excel_entry.set_args(upload_instance, file_path)
    assert db_excel_entry.upload_instance == upload_instance
    assert db_excel_entry.file_path == file_path


def test_read_excel_to_dict(db_excel_entry, test_excel_file):
    """ Проверяем на выходе, что это генератор содержащий словари """
    db_excel_entry.file_path = test_excel_file   # Добавление в экземпляр необходимых аргументов
    result_generator = db_excel_entry.read_excel__to_dict()    # Вызов тестируемого метода
    assert isinstance(result_generator, Generator)
    n = next(result_generator)
    assert isinstance(n, dict)


def test_router(db_excel_entry, generate_random_data):
    """ Проверяем, что результат генератора соответствует ожидаемому формату """
    generator = generate_random_data
    # Вызов тестируемого метода
    result_generator = db_excel_entry.router(generator)
    assert isinstance(result_generator, Generator)
    for result_row in result_generator:
        assert isinstance(result_row, list)
        for data in result_row:
            assert isinstance(data, dict)
            for model, fields in data.items():
                assert issubclass(model, models.Model)
                assert isinstance(fields, dict)

def test_validate(db_excel_entry, generate_random_data):
    """ Здесь мы изменяем значение поля что бы валидация не прошла """
    data = next(generate_random_data)
    data['numberlist'] = 'sadasd'       # подкидываем значение не которое не пройдёт валидацию
    cortej = db_excel_entry.aggregator.mytuple
    with pytest.raises(ValidationError):
        db_excel_entry.validate(item={cortej[0][0]: data}, validator=cortej[0][1])

def test_check_fields(db_excel_entry):
    """ Здесь мы изменяем соответствие между полями модели и валидатором что б проверка не прошла """
    cortej = db_excel_entry.aggregator.mytuple
    model_fields = cortej[0][0]._meta.get_fields()
    validator = cortej[1][1]     # меняем валидатор соответствующий модели на другой, этим эмулируем не совпадение полей
    with pytest.raises(Exception):
        db_excel_entry.check_fields(model_fields, validator)

@pytest.mark.django_db
def test_entry_to_db(db_excel_entry):
    """ В целом ничего не проверяет """
    print(connection.settings_dict['NAME'])
    def generator():
        yield {'Model1': {'field1': 'value1', 'field2': 'value2'}},  {'Model2': {'field3': 'value3', 'field4': 'value4'}}
        yield {'Model1': {'field1': 'value5', 'field2': 'value6'}},  {'Model2': {'field3': 'value3', 'field4': 'value4'}}
    db_excel_entry.similar_batch_size = 10
    db_excel_entry.N = 5
    db_excel_entry.objects_to_create = MagicMock()
    with suppress(AttributeError):
        db_excel_entry.entry_to_db(generator())
    # db_instance.objects_to_create.assert_called()
#


