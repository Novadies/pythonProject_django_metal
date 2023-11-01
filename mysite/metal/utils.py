from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.paginator import Paginator

from metal.forms import MetalForm
from metal.sourse.menu import menu


class If_paginator():
    def if_paginator(self, request):
        paginator = Paginator(*self.to_padinator, orphans=5)
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

class NoSlugMixin():  # тут конкретно нет смысла передавать больше чем одну модель во View, но да ладнo
    template, to_padinator = None, None
    dict_dop, Data ={},{}

    def get(self, request):
        dict_context = {model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()}  # передаются экземпляры класса
        if self.to_padinator: dict_context = {**dict_context, **self.if_paginator(request)}
        context={**dict_context, **self.dict_dop}  # передаются дополнительные параметры, например формы
        return render(request, self.template, context=context)

class SearchMixin():
    template_name = 'metal/search.html'
    form_class = MetalForm
    def get_context_data(self, initial=False, **kwargs): #перенёс сюда, потому что могу, добавил initial для поста запроса
        context = super().get_context_data(**kwargs)
        context['initial'] = initial if initial else {field: getattr(self.object, field, None) for field in self.form_Meta.fields}
        context['form'] = self.form_class(extra_data=context['initial'])
        return context

class ContextMixin():
    pass