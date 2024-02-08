import warnings

def true_or_None (clean_data: dict, fields_to_check: list) -> dict:
    """ заменяет пустую строку на None """
    for field in fields_to_check:
        if field in clean_data and clean_data[field] == "":
            clean_data[field] = None
    return clean_data

def catch_warnings_simplefilter_ignore(funk, *args, **kwargs):
    """ Убрать предупреждения """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        funk(*args, **kwargs)

