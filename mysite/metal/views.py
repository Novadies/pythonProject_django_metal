from itertools import chain

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, FormView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from django_filters.views import FilterView

from .filters import Metal_infoFilter
from .forms import ContactForm
from .signals import must_send_mail_signals
from .tools.decorators2 import track_queries
from .tools.logic_for_NewStart import save_in_session, get_field_from_model, save_to_db, save_in_cookies

from .tools.simple_send_mail import send_results_by_email
from .utils import *
from .models import *
if settings.DEBUG: from .tools.for_null_db import *

class NewStart(DecoratorContextMixin, ListView):
    paginate_by = 20
    paginate_orphans = 5
    model = Metal_info
    template_name = "metal/start.html"

    def get_queryset(self):
        """ Можно использовать prefetch_related, делает на 1 запрос больше чем select_related, но по времени ~ тоже самое """
        return self.model.count_manager.select_related("metals_class").all()


class NewSearch(View):
    """ вьюха разделяется на 2. Для обработки отдельно post и get запросов """
    def get(self, request, *args, **kwargs):
        view = GetSearch.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSearch.as_view()
        return view(request, *args, **kwargs)


class GetSearch(SearchMixin, SingleObjectMixin, ListView, FormMixin):
    paginate_by = 15
    paginate_orphans = 5

    decorators = [track_queries]

    def get_paginate_by(self, queryset):
        if self.kwargs:  # что б не было ошибки если нечего отображать
            return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_name'] = 'search_form'
        context['model_fields'] = self.form_Meta.fields
        return context

    def get_initial(self):
        """ Начальные значения для формы """
        initial = super().get_initial()
        initial.update({field: getattr(self.object, field, None) for field in self.form_Meta.fields})
        initial['mail_checkbox'] = self.request.session.get('mail_checkbox', False) # сохранение состояния mail_checkbox происходит только при POST запросах
        # checkbox = 'mail_checkbox'     # fixme c куками не работает
        # initial[checkbox] = value_in_cook if \
        #     (value_in_cook := self.request.COOKIES.get(checkbox, None)) is not None \
        #     else self.request.session.get(checkbox, False)
        return initial

    def get_queryset(self):
        if self.object is not None:
            return self.object.metals_info.select_related(
                "metals_class", "metals").all()  # здесь выбирается кверисет , который будет page_obj

    def get(self, request, *args, **kwargs):
        """ начальные значения для формы """
        self.object = self.get_object()          # необходимо явно прописать self.object так как основной класс ListView
        response = super().get(request, *args, **kwargs) # что бы получить self.object_list нужно вызвать get()

        if not request.user.is_staff:                           # отправка сообщения на страницу
            messages.add_message(request, messages.INFO, f"Нравится этот сервис?\nПопробуйте получить результыты по почте", fail_silently=True)
        else:
            send_results_by_email(request, self.object_list)

        return response

    def get_object(self, queryset=None):
        if self.kwargs:
            queryset = self.form_Meta.model.objects.all()
            return super().get_object(queryset=queryset)

class PostSearch(SearchMixin, CreateView):
    decorators = [track_queries]

    def form_valid(self, form):
        """ добавляем данные с формы, а так же сгенерированые самостоятельно """
        save_in_session(self, form, name_in_session='mail_checkbox')

        dop_field = get_field_from_model(self)
        save_to_db(self, form, dop_field)
        response = HttpResponseRedirect(reverse("search-slug-url", args=[dop_field["slug"]]))
        # save_in_cookies(self, form, response, name_in_cookie='mail_checkbox')
        return response

    # def form_invalid(self, form):
    # в случае если форма не прошла, можно перезанрузить страницу с исправленными данными (нужно определить get_context_data)
    #     return render(self.request, self.template_name, self.get_context_data(initial=form.cleaned_data))


class Steel_class(DecoratorContextMixin, ListView):
    paginate_by = 12
    paginate_orphans = 5
    model = Metal_class
    template_name = "metal/steel-steel_class.html"

    def get_queryset(self):
        return self.model.objects.order_by("steel_class")


class Steel(DecoratorContextMixin, DetailView):
    model = Metal_info
    template_name = "metal/steel-slug.html"
    context_object_name = "metal_info"


class Steel_class_slug(DecoratorContextMixin, SingleObjectMixin, ListView):
    template_name = "metal/steel-steel_class-slug.html"
    paginate_by = 8
    paginate_orphans = 2
    slug_model = Metal_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.slug_model.__name__.lower()] = self.object  # определяем имя, оно используется в шаблоне
        return context

    def get(self, request, *args, **kwargs):
        """ Явно указываем queryset, иначе будет искать в get_queryset() """
        self.object = self.get_object(queryset=self.slug_model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):  # тут object, а не менеджер objects
        return self.object.metals_info.all()  # здесь выбирается кверисет , который будет page_obj


class SearchAll(LoginRequiredMixin, DecoratorContextMixin, ListView):
    paginate_by = 20
    paginate_orphans = 5
    model = MetalSearch
    template_name = "metal/steel-result.html"

    def get_queryset(self):
        """ Используется кэш cache.get_or_set """
        queryset = self.model.count_manager.filter(user_search=self.request.user.pk).order_by("-date")
        # todo  о кэше. Нужно обязательно предусматривать реализацию удаления кэша. Можно удалять кэш используя сигналы.
        #  Имена кэша можно хранить в сеттингс, или возможно в другом целевом корневом файле, что бы обращаться к нему без проблем
        #queryset = cache.get_or_set('searchall', queryset, 60)     # кэшировать здесь так себе идея
        return queryset


class SearchView(ListView):  # todo поиск по сайту должен быть используя контент тайп или типо того и может он долен быть как отдельное приложение?
    paginate_by = 10
    paginate_orphans = 5
    template_name = "metal/search_list.html"
    model = Metal_class

    def get(self, request, *args, **kwargs):
        self.query = request.GET.get("search_in_bar", "")  # Получаем значение параметра запроса из формы в бэйс форм
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        return context

    def get_queryset(self):
        """ поиск по определённым полям модели """
        if q := self.query:
            queryset1 = self.model.objects.filter(
                steel_class__icontains=q)
            queryset2 = Metal_info.objects.filter(
                steel__icontains=q)
            queryset = list(chain(queryset1, queryset2))
            logger.debug(queryset)
        else:
            queryset = self.model.objects.none()
        return queryset

class SearchMoreView(FilterView):
    """
    Представление для работы с фильтром.
    Для корректной работы пагинации необходимо использовать
    templatetags.custom_filter_tag.param_replace"""
    paginate_by = 10
    paginate_orphans = 5
    template_name = "metal/search_list_more.html"
    filterset_class = Metal_infoFilter


class ContactFormView(FormView):
    """ Форма обратной связи """
    form_class = ContactForm
    template_name = 'metal/feedback.html'
    success_url = reverse_lazy('start-url')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_name'] = 'contact_form_submission'   # подключение капчи
        return context

    def form_valid(self, form):
        #debug.info(form.cleaned_data)
        must_send_mail_signals.send(sender=self.__class__, form=form)
        return super().form_valid(form)
