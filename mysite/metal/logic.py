from django.db.models import QuerySet
def If_0_value(answer: QuerySet, cleaned_data: dict)-> QuerySet:
    data_0 = [key for key, value in cleaned_data.items() if value == 0]
    if data_0:
        data_min_0 = [f'{key}_min' for key in data_0]
        for key in data_min_0:
            key_model = {key: float(0)}
            answer = answer.filter(**key_model)
    return answer

