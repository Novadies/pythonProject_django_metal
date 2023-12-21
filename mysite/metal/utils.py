from functools import reduce

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.core.paginator import Paginator

from metal.forms import MetalForm
import logging

logger = logging.getLogger('metal')

class If_paginator:
    def if_paginator(self, request):
        paginator = Paginator(*self.to_padinator, orphans=5)
        page = paginator.get_page(request.GET.get("page", 1))
        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = f"?page={page.previous_page_number()}"
        else:
            prev_url = ""
        if page.has_next():
            next_url = f"?page={page.next_page_number()}"
        else:
            next_url = ""
        context = {
            "page_object": page,
            "is_paginated": is_paginated,
            "next_url": next_url,
            "prev_url": prev_url,
        }
        return context


class NoSlugMixin:  # тут конкретно нет смысла передавать больше чем одну модель во View, но да ладнo
    template, to_padinator = None, None
    dict_dop, Data = {}, {}

    def get(self, request):
        dict_context = {
            model.__name__.lower(): get_list_or_404(qset)
            for model, qset in self.Data.items()
        }  # передаются экземпляры класса
        if self.to_padinator:
            dict_context = {**dict_context, **self.if_paginator(request)}
        context = {
            **dict_context,
            **self.dict_dop,
        }  # передаются дополнительные параметры, например формы
        return render(request, self.template, context=context)


class SearchMixin:
    template_name = "metal/search.html"
    form_class = MetalForm
    paginate_by = 20
    paginate_orphans = 10


class DecoratorContextMixin:
    """ миксин применяющий список из декораторов для декорирования класса """

    def dispatch(self, *args, **kwargs):
        """ применяем список с декораторами к dispatch (а значит и к вьюхе по цепочке) """
        decorators = getattr(self, 'decorators', [])
        base = super().dispatch
        for decorator in decorators:
            if callable(decorator):  # Проверка, что декоратор вызываемый объект
                base = decorator(base)
            else:
                logger.warning(f'Ошибка, {decorator} не декоратор')
        return base(*args, **kwargs)

class UserPassesTestMixin:
    def user_passes_test(self, user):
        return user.is_authenticated()

    def user_failed_test(self):
        return redirect("LOGIN_URL")

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request.user):
            return self.user_failed_test()
        return super().dispatch(request, *args, **kwargs)

class BaseView: # вообще это в мидлвеар по смыслу надо засовывать
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception:
            return self._response({'errorMessage': Exception.message}, status=400)
        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response
    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list),
            json_dumps_params={'ensure_ascii': False}
        )
