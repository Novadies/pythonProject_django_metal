from django.db.models import QuerySet, Q

def packing(data: str) -> str:
    # упаковка полученных значений из формы в бд, учитывая знак "-"
    *raw_value, value2 = data.split("-")
    if len(raw_value) == 1:
        return f"{float(raw_value[-1])}-{float(value2)}" if raw_value[0] else float(f"-{value2}")
    else:
        return f"-{float(raw_value[-1])}-{float(value2)}" if raw_value else float(value2)

def query_method(exist, answer):
    return answer.exclude if exist else answer.filter

def If_0_value(answer: QuerySet, cleaned_data: dict)-> QuerySet:
    # обработка нулевых значений
    data_0 = {key: value for key, value in cleaned_data.items() if value == 0}
    if data_0:
        for key, value in data_0.items():
            prefix = str(value).startswith('-')
            key = f'{key}_min'
            value = float(str(value)[1:]) if prefix else float(value)
            answer = query_method(prefix, answer)(**{key: value})
    return answer

def other_value(answer: QuerySet, data: dict, key: str)-> QuerySet:
    dk = data[key]
    if isinstance(dk, float): # если значение одно число
        prefix = str(dk).startswith('-')
        value = float(str(dk)[1:]) if prefix else dk
        key_model_lte = {f'{key}_min__lte': value}
        key_model_gte = {f'{key}_max__gte': value}
        answer = query_method(prefix, answer)(**key_model_lte, **key_model_gte)
    else: #если значение диапазон
        *prefix, value1, value2 = dk.split("-")
        key_model_min__range = {f'{key}_min__range': (float(value1), float(value2))}
        key_model_max__range = {f'{key}_max__range': (float(value1), float(value2))}
        answer = query_method(prefix, answer)(Q(**key_model_min__range) | Q(**key_model_max__range))
    return answer
