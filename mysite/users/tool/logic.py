def true_or_None (model, fields_to_check):
    """ заменяет пустую строку на None """
    for field in fields_to_check:
        if hasattr(model, field) and getattr(model, field) == "":
            setattr(model, field, None)
