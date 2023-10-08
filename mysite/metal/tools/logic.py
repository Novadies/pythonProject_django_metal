from django.db.models import QuerySet, Q


def packing(data: str) -> str:
    *raw_value, value2 = data.split("-")
    if len(raw_value) == 1:
        return f"{float(raw_value[-1])}-{float(value2)}" if raw_value[0] else float(f"-{value2}")
    else:
        return f"-{float(raw_value[-1])}-{float(value2)}" if raw_value else float(value2)

def If_0_value(answer: QuerySet, cleaned_data: dict)-> QuerySet:
    data_0 = {key: value for key, value in cleaned_data.items() if value == 0}
    if data_0:
        for key, value in data_0.items():
            key = f'{key}_min'
            query_method = answer.exclude if str(value).startswith('-') else answer.filter
            value = float(str(value)[1:]) if str(value).startswith('-') else float(value)
            answer = query_method(**{key: value})
    return answer

def other_value(answer: QuerySet, data: dict, key: str)-> QuerySet:
    dk = data[key]
    if type(dk)==float:
        first = str(dk).startswith('-')
        value = float(str(dk)[1:]) if first else dk
        query_method = answer.exclude if first else answer.filter
        key_model_lte = {f'{key}_min__lte': value}
        key_model_gte = {f'{key}_max__gte': value}
        return query_method(**key_model_lte, **key_model_gte)
    else:
        *hyphen, value1, value2 = dk.split("-")
        query_method = answer.exclude if hyphen else answer.filter
        key_model_min__range = {f'{key}_min__range': (float(value1), float(value2))}
        key_model_max__range = {f'{key}_max__range': (float(value1), float(value2))}
        return query_method(Q(**key_model_min__range) | Q(**key_model_max__range))