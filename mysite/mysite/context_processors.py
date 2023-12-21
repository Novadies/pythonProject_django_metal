from static.menu import menu2


def get_menu(request) -> dict:
    """ общий для проекта контекст процессор """
    context = {}
    exclude = ['simple_history', 'silk', 'django_filters', 'debug_toolbar']
    r = request.resolver_match
    if r and r.app_name not in exclude:
        template_name = r.url_name
        context['menu'] = menu2.get(template_name, 'Страница')
    return context
