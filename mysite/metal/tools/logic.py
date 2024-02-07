from typing import Optional, Tuple, Type, Callable

from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Q
from django.utils.timezone import make_aware

from logs.logger import logger
from metal.models import Metal, Metal_info, Metal_2
from django.utils.datetime_safe import datetime

import re
import logging


def get_field_from_model(model, *, str_date="date", str_slug='slug', user_search_id='user_search_id') -> dict:
    """ текущая дата, slug на её основе, привязка к текущему user """
    date = make_aware(datetime.now())
    slug = str(date)[-21:-6].replace(":", "_").replace(".", "-")
    user_search = model.request.user.pk
    return {str_date: date, str_slug: slug, user_search_id: user_search}


def save_to_db(model, form, /, *args: dict) -> None:
    """ так как нужно добавить значения,
     кроме тех, что в форме,то обрабатываем формы вручную"""
    """ unpacked_dicts по умолчанию есть get_field_from_model(), однако предусмотрено получение нескольких словарей"""
    unpacked_dicts = {key: value for dictionary in args for key, value in
                      dictionary.items()}  # распаковка кортежа из словарей в один мега словарь
    form.cleaned_data = {key: value for key, value in form.cleaned_data.items()
                         if
                         key in model.form_Meta.fields}  # очистка данных для сохранения в модель от не модельных полей
    for_save_to_db = model.form_class.Meta.model.objects.create(  # создание строки в MetalSearch
        **unpacked_dicts, **form.cleaned_data)
    connections = _search_for_connections(form.cleaned_data)
    for_save_to_db.metals_info.add(*connections)  # создание связей


def _search_for_connections(cleaned_data: dict, model=Metal_2) -> QuerySet:
    """ОБРАБОТКА значений из формы после валидации """
    data = {key: value for key, value in cleaned_data.items() if value}    # получение всех значений кроме нулевых
    # only = collapse([[f'{key}_min', f'{key}_max'] for key in data]) # перечень полей которые есть в запросе формы
    # logger.info(data)
    only = {}
    answer = model.objects.only(*only)
    answer = If_0_value(answer, cleaned_data)  # обработка нулевых значений
    if data:
        for key in data:
            answer = other_value(answer, data, key)
    return Metal_info.objects.filter(metals__metal_compound__in=answer)  # проход по связям таблиц


def query_method(exist: str, answer: QuerySet):
    """ выбор между exclude и filter"""
    return answer.exclude if exist else answer.filter


def If_0_value(answer: QuerySet, cleaned_data: dict) -> QuerySet:
    """ обработка нулевых значений """
    data_0 = {key: value for key, value in cleaned_data.items() if value == 0}
    if data_0:
        for key, value in data_0.items():
            prefix = str(value).startswith('-')
            key = f'{key}_min'
            value = float(str(value)[1:]) if prefix else float(value)
            answer = query_method(prefix, answer)(**{key: value})
    logger.debug(answer)
    return answer


def other_value(answer: QuerySet, data: dict, key: str) -> QuerySet:
    """ основной обработчик значений"""
    dk = data[key]
    if isinstance(dk, float):  # если значение одно число
        prefix = str(dk).startswith('-')
        value = float(str(dk)[1:]) if prefix else dk
        key_model_lte = {f'{key}_min__lte': value}
        key_model_gte = {f'{key}_max__gte': value}
        answer = query_method(prefix, answer)(**key_model_lte, **key_model_gte)
    else:  # если значение диапазон
        *prefix, value1, value2 = dk.split("-")
        key_model_min__range = {f'{key}_min__range': (float(value1), float(value2))}
        key_model_max__range = {f'{key}_max__range': (float(value1), float(value2))}
        answer = query_method(prefix, answer)(Q(**key_model_min__range) | Q(**key_model_max__range))
    logger.debug(answer)
    return answer


def process_cleaned_data(cleaned_data: dict):
    """Генератор обработки очищенных данных формы."""
    # Проверка наличия нулевых полей и генерация ошибок
    what_about_null_fields(cleaned_data, any)
    # Проверка каждого поля на наличие ошибок валидации
    for f, v in ((f, v) for f, v in dict(cleaned_data).items() if v):  # исключение пустых полей
        errors = validation_for_field_in_clean(v)
        if errors is not None:
            yield f, errors
        else:
            cleaned_data[f] = cleaned_data_replace(v)


def what_about_null_fields(cleaned_data: dict, logic):
    """принимает словать и логическую функцию, например any или all"""
    if not logic(cleaned_data.values()):
        raise ValidationError("Недостаточное количество полей заполено")


def validation_for_field_in_clean(value: str) -> Optional[ValidationError]:
    """ валидация поля для цикла в методе clean """

    if len(value) > 12:
        return ValidationError("Длина превышает 12 символа")

    if not _get_pattern().match(value):
        return ValidationError("Введите подходящее число")


def _get_pattern(pattern=None):
    """ шаблон для валидации"""
    default = re.compile(
        r"^([-—]?\d{1,2}([.,$]\d{0,2})?)([-—]\d{1,2}([.,$]\d{0,2})?)?$")  # проверка учитывающая ввод диапазона
    return pattern or default


def cleaned_data_replace(data: str) -> str:
    """ очистка данных от некорретных символов """
    data = data.replace(",", ".").replace(" ", "").replace("—", "-")
    *raw_value, value2 = data.split("-")
    if len(raw_value) == 1:
        string = f"{float(raw_value[-1])}-{float(value2)}" if raw_value[0] else float(f"-{value2}")
    else:
        string = f"-{float(raw_value[-1])}-{float(value2)}" if raw_value else float(value2)
    logger.debug(string)
    return string

def save_in_session(model, form, in_session: str):
    """ Сохранение в сессию значения из поля in_session, по этому ключу """
    if model.request.session.get(in_session, None) is not (value := form.cleaned_data[in_session]):
        model.request.session[in_session] = value
