from functools import wraps

from django.core.paginator import Paginator
from django.db import connection


def if_paginator(to_padinator, request):
    paginator = Paginator(*to_padinator, orphans=5)
    page = paginator.get_page(request.GET.get('page', 1))
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ''
    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ''
    context = {'page_object': page,
               'is_paginated': is_paginated,
               'next_url': next_url,
               'prev_url': prev_url
               }
    return context

#Декоратор из класса
class If_paginator:
    # запоминаем аргументы декоратора
    def __init__(self, dict_dop, to_padinator):
        self.dict_dop = dict_dop
        self.to_padinator = to_padinator
    # декоратор общего назначения
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.dict_dop.update(if_paginator(self.to_padinator, args[1]))
            val = func(*args, **kwargs)
            return val
        return wrapper


# аналогичный обычный декоратор
def decorator_with_arguments(dict_dop, to_padinator):
    print(to_padinator)
    def my_decorator(func):
        def wrapped(*args, **kwargs):
            dict_dop.update(if_paginator(to_padinator, args[1]))
            return func(*args, **kwargs)

        return wrapped
    return my_decorator


def track_queries(func):
    # использование connection в качестве декоратора
    @wraps(func)
    def wrapper(*args, **kwargs):
        q = len(connection.queries)
        func_return = func(*args, **kwargs)
        print(func.__name__)
        executed_queries = connection.queries[q:]
        time = 0
        for n, queri in enumerate(executed_queries):
            print(f'{n + 1}___________{queri}')
            time += float(queri['time'])
        else:
            print(time)
        return func_return
    return wrapper