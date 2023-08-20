from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.paginator import Paginator
from .decorators import decorator_with_arguments
class If_paginator():
    to_padinator = None
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

class NoSlugMixin(If_paginator):  # тут конкретно нет смысла передавать больше чем одну модель во View, но да ладно
    models_for_data, Qset = [],[]
    template = None
    dict_dop, Data ={},{}
    if Qset: Data = dict(zip(models_for_data, Qset))
    def get(self, request):
        dict_context = {model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()}  # передаются экземпляры класса
        if self.to_padinator: dict_context.update(self.if_paginator(request))
        context={**dict_context, **self.dict_dop}  # передаются дополнительные параметры, например формы
        return render(request, self.template, context=context)

class ForSlugMixin():
    model=None
    template= None
    def get(self, request, slug):
        context={self.model.__name__.lower(): get_object_or_404(self.model, slug__iexact=slug)} # передаётся экземпляр класса
        return render(request, self.template, context=context)