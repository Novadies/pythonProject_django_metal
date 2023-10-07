from django.db.models import QuerySet
def If_0_value(answer: QuerySet, cleaned_data: dict)-> QuerySet:
    data_0 = {key: value for key, value in cleaned_data.items() if value == 0}
    if data_0:
        for key, value in data_0.items():
            key = f'{key}_min'
            query_method = answer.exclude if str(value).startswith('-') else answer.filter
            value = float(str(value)[1:]) if str(value).startswith('-') else value
            answer = query_method(**{key: value})
    return answer

def single_value(answer: QuerySet, data: dict, key: str)-> QuerySet:
    dk = data[key]
    first = str(dk).startswith('-')
    value = float(str(dk)[1:]) if first else dk
    query_method = answer.exclude if first else answer.filter
    key_model_lte = {f'{key}_min__lte': value}
    key_model_gte = {f'{key}_max__gte': value}
    return query_method(**key_model_lte, **key_model_gte)