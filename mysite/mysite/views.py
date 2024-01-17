from functools import wraps

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def decorator_redirect_page(name):
    """ Декоратор для redirect_page """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs, name=name)
            return result
        return wrapper
    return decorator

def pagenotfound(request, exeption):
    return render(request, '404.html', status=404)

def redirect_page(request, name='start-url'):
    """ Редирект, применяется с декоратором """
    return HttpResponseRedirect(reverse(name))
