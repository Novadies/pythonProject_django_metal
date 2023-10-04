from django.http import HttpResponseNotFound


def pagenotfound(request, exeption):
    return HttpResponseNotFound('<h1>Страница не найдена!</h1>')