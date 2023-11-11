from django.urls import resolve

from metal.forms import SearchForm
from metal.sourse.menu import menu2
def get_menu(request):
    # print(resolve(request.path_info))
    context = {}
    #context['form_search'] = SearchForm
    if request.path.split('/')[1] == 'metal':
        template_name = request.resolver_match.url_name
        context['menu'] = menu2.get(template_name, 'Страница')
    return context