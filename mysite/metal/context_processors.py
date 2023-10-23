from metal.sourse.menu import menu2
def get_menu(request):
    template_name = request.resolver_match.url_name
    context ={'menu' : menu2.get(template_name, 'Страница')}
    return context