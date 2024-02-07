import time

from functools import wraps
from icecream import ic

from django.db import connection

from logs.logger import logger


def print_decorator(func):
    def wrapper(*args, **kwargs):
        ic('Тест1')
        func_return = func(*args, **kwargs)
        ic('Тест2')
        return func_return
    return wrapper

def track_queries(func):
    """Декоратор для вывода SQL запросов"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()  # Запускаем таймер до вызова функции
            q = len(connection.queries)
            func_return = func(*args, **kwargs)
            end_time = time.time()  # Запускаем таймер после вызова функции
            executed_queries = connection.queries[q:]
            total_time = end_time - start_time  # Вычисляем общее время выполнения
            ic(total_time)
            ic(func.__name__)
            for n, query in enumerate(executed_queries):
                print(f"{n + 1}--{query}")
            return func_return
        except Exception:
            logger.warning(f'Декоратор track_queries не сработал, {func} не была декорирована')
            return func(*args, **kwargs)
    return wrapper
