import pandas as p

from contextlib import suppress
from typing import List, Dict, Any, Generator, Type, Literal, Optional, Union

from funcy import print_durations
from pydantic import ValidationError, BaseModel
from itertools import count

from django.db.models import Model
from django.db import transaction

from loader.models import Aggregator
from logs.logger import log_metal


class DB_ExcelEntry:
    """ Базовый класс для записи из эксель.
        objects_to_create() требует переопределения в случае работы с разными моделями
    """
    def __init__(self,
                 aggregator: Aggregator = None,     # экземпляр содержащий модели и их валидаторы
                 upload_instance=None,              # сам файл
                 file_path=None,                    # путь к файлу
                 engine: Literal["Pandas", "Polars"] = "Pandas",
                 is_validate: bool = True,          # нужна ли валидация
                 check_compliance: bool = True,     # нужно ли проверять соответствие полей перед валидацией
                 N: Optional[int] = 10,             # число строк которые загрузит bulk_create
                 similar_batch_size: Optional[int] = 999,   # поведение подобно batch_size в bulk_create
                 sheet: Optional[str] = None,       # наименование нужной страницы
                 header: bool = True,               # есть ли заголовок, помимо самих наименований полей (это не заголовок)
                 value: str = '',                   # как записываются пустые строки
                 ):
        self.aggregator = aggregator
        self.upload_instance = upload_instance
        self.file_path = file_path
        self.engine = engine
        self.is_validate = is_validate
        self.check_compliance = check_compliance
        self.N = N
        self.similar_batch_size = similar_batch_size
        self.sheet = sheet
        self.header = header
        self.value = value

    def set_args(self, upload_instance, file_path):
        """ Что бы определить аргументы позже """
        self.upload_instance = upload_instance
        self.file_path = file_path

    @print_durations('ms', threshold=0.01)
    def read_excel__to_dict(self, orient='records', inplace=True) -> Generator:
        """ На вход получаем адрес файла, а на выходе генератор из словарей"""
        # match engine:               # 3.10
        #     case "Pandas":
        #         import pandas as p
        #     case "Polars":
        #         import polars as p
        #         p.default_options().na = self.value

        """ df это генератор """
        try:
            """
            read_excel возвращает либо DataFrame, либо словарь из них, если указан множественный выбор страниц (например None),
            но такой вариант вероятно смысла рассматривать нет, поэтому sheet_name это либо поведение по умолчанию, либо имя страницы
            """
            sheet_name = self.sheet or 0
            df = p.read_excel(self.file_path, sheet_name=sheet_name)   # sheet_name=None пытается загрузить все страницы
        except Exception:
            df = p.read_csv(self.file_path)
        with suppress(Exception):
            df.fillna(value=self.value, inplace=inplace)                # указываем значения в пустых ячейках
        row_list_dict = df.to_dict(orient=orient)
        yield from row_list_dict[1:] if self.header else row_list_dict  # если есть заголовок, убираем его

    @print_durations('ms', threshold=0.01)
    def router(self, generator: Generator) -> Generator:
        """ Разделяем генератор по структурным частям, в соответствии с моделями, то есть читаем его, обрабатываем, передаём дальше
        Ключи в генераторе были кортежем (model, validator), а стали просто model.
        """
        for item in generator:
            result_row = []
            for instance in self.aggregator.mytuple:        # Получаем кортежи (модель - валидатор) из класса Aggregator
                model, validator = instance
                model_fields = model._meta.get_fields()
                if self.check_compliance:                                  # проверка полей модели и валидатора
                    self.check_fields(model_fields, validator)
                """ Если в документе существуют посторонние поля, они отсекаются """
                data = {model: {key: value for key, value in item.items() if key in [field.name for field in model_fields]}}
                data = self.validate(data, validator) if self.is_validate else data              # валидация пайдентиком
                result_row.append(data)
            self.check_compliance = False                       # для того что бы не проверять по десять раз одно и тоже
            yield result_row

    @print_durations('ms', threshold=0.01)
    def entry_to_db(self, generator: Generator) -> None:
        """ Собираем N строк от генератора и записываем bulk_create-ом"""
        scope = range(self.N) if self.N is not None and isinstance(self.N, int) else count(0)
        with transaction.atomic():
            try:
                while True:
                    if_break = False  # флаг для break
                    data_dict = {}
                    for i in scope:
                        items = next(generator)                                         # итерация по генератору
                        if items:
                            for item in items:  # print_iter_durations(items):             # итерация по 'моделям'
                                (model, model_data), = item.items()
                                if model not in data_dict:
                                    data_dict[model] = []  # Если модель не встречалась ранее, создаем пустой список для нее
                                data_dict[model].append(model_data)
                                if self.similar_batch_size and i * len(model_data) > self.similar_batch_size:
                                    if_break = True
                        if if_break:                    # выход из цикла for если значений больше чем similar_batch_size
                            break
                    self.objects_to_create(data_dict)                   # записываем в бд в конце каждой итерации while
            except StopIteration:
                self.upload_instance.db_record = self.upload_instance.STATUS.published
                self.upload_instance.save()                             # изменяем статус загруженного файла
                if data_dict:                           # Если остались объекты после окончания генерации, записываем их
                    self.objects_to_create(data_dict)

    #@print_durations('ms', threshold=0.01)
    def objects_to_create(self, _dict: dict) -> None:
        # fixme в текущей реализации нет связей между собою между загружаемыми моделями, так как связи могут быть разными,
        # fixme то для разных вариантов загружаемых моделей нужно переопределять objects_to_create() и не забывать создавать связи в моделях
        """
        Запись в бд с помощью  bulk_create.
        Данный метод вероятно придётся переопределять если загружать другие файлы
        """
        for model, list_data in _dict.items():
            objects = (model(**item, to_uploader=self.upload_instance, to_user=self.upload_instance.to_user)
                       for item in list_data)  # добавлена связь на модель загрузчика и юзера
            model.objects.bulk_create(objects)


    @staticmethod
    @print_durations('ms', threshold=0.01)
    def check_fields(model_fields: List[Model], validator: Type[BaseModel]):
        """ Поля модели и поля его валидатора должны совпадать """

        def exclude(input_fields: List[Model], *args: str) -> list:
            """ Получение полей из модели исключая определенные """
            return [field.name for field in input_fields
                    if not any([field.one_to_one, field.many_to_many, field.many_to_one, field.one_to_many])
                    and field.name not in ["id", *args]]
        
        mod_fields = exclude(model_fields)
        val_fields = list(validator.model_fields)
        if mod_fields != val_fields:
            raise Exception(f'Не соответствие между существующими полями модели {mod_fields} и полями его валидатора {val_fields}')


    @staticmethod
    @print_durations('ms', threshold=0.01)
    def validate(item: dict, validator: Type[BaseModel]) -> dict:
        """ Валидация данных перед генерацией значения.
        ! Валидация проваливается если предоставлены не все поля модели в загруженном документе !
        """
        (model, data), = item.items()
        val_data = validator.model_validate(data)
        return {model: val_data.model_dump()}
