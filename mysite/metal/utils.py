from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.paginator import Paginator

class If_paginator():
    to_padinator = None
    #@staticmethod  # или classmethod  ?
    def if_paginator(self, request):

        paginator = Paginator(self.to_padinator, '20', orphans=5)
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
 #TODO: может для пагинации сделать декоратор  класса?
class NoSlugMixin(If_paginator):  # тут конкретно нет смысла передавать больше чем одну модель во View, но да ладно
    models=[]
    template = None
    dict_dop, Data ={},{}

    def get(self, request):

        if self.to_padinator:
            dict_context = self.if_paginator(request)
        else:
            dict_context={model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()} #передаются экземпляры класса

        context={**dict_context, **self.dict_dop}  # передаются дополнительные параметры, например формы
        return render(request, self.template, context=context)

class ForSlugMixin():
    model=None
    template= None
    def get(self, request, slug):
        context={self.model.__name__.lower(): get_object_or_404(self.model, slug__iexact=slug)} # передаётся экземпляр класса
        return render(request, self.template, context=context)