from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.views.generic import View, ListView, FormView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import make_aware


from .forms import *
from .tools.decorators2 import track_queries
from .utils import *


# class Start(NoSlugMixin, If_paginator, View):
#     models = [Metal_info]
#     to_padinator = (models[0].count_manager.all(), '40')
#     template = 'metal/start.html'
#     dict_dop = {'menu': menu[template]}

class NewStart(ContextMixin, ListView):
    paginate_by = 20
    paginate_orphans =5
    model = Metal_info
    template_name = 'metal/start.html'
    def get_queryset(self):
        # prefetch_related делает на 1 запрос больше чем select_related, но в итоге быстрее раза в 3
        return self.model.count_manager.prefetch_related('metals_class').all()

class NewSearch(View):
    @track_queries
    def get(self, request, *args, **kwargs):
        view = GetSearch.as_view()
        return view(request, *args, **kwargs)

    @track_queries
    def post(self, request, *args, **kwargs):
        view = PostSearch.as_view()
        return view(request, *args, **kwargs)

class GetSearch(SearchMixin, ContextMixin, SingleObjectMixin, ListView):
    paginate_by = 15
    paginate_orphans = 5
    form_class = MetalForm
    form_Meta = form_class.Meta
    def get_paginate_by(self, queryset):
        if self.kwargs: # что б не было ошибки если нечего отображать
            return self.paginate_by

    def get_initial(self): #начальные значения для формы
        if self.kwargs:
            return self.get_object(queryset=self.form_Meta.model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['initial'] = {field: getattr(self.object, field, None) for field in self.form_Meta.fields}
        context['form'] = self.form_class(extra_data=context['initial'])
        return context

    def get_queryset(self):
        if self.object:
            return self.object.metals_info.select_related('metals_class', 'metals').all() # здесь выбирается кверисет , который будет page_obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_initial() #ачальные значения формы
        return super().get(request, *args, **kwargs)


class PostSearch(SearchMixin, CreateView):
    @staticmethod
    def get_dop_field():
        date = make_aware(datetime.now())
        slug = str(date)[-21:-6].replace(':', '_').replace('.', '-')
        return date, slug

    def form_valid(self, form):
        dop_field={'slug': self.get_dop_field()[1], 'date': self.get_dop_field()[0]}
        # добавляем данные с формы, а так же сгенерированые самостоятельно
        for_save_to_db = self.form_class.Meta.model.objects.create(**dop_field, **form.cleaned_data) #так как нужно добавить значения,
        # кроме тех, что в форме,то обрабатываем формы вручную
        connections = self.form_class.search_for_connections(form.cleaned_data)
        for_save_to_db.metals_info.add(*connections)
        return HttpResponseRedirect(reverse('search-slug-url', args=[dop_field['slug']]))


class Steel_class(ContextMixin, ListView):
    paginate_by = 12
    paginate_orphans =5
    model = Metal_class
    template_name = 'metal/steel-steel_class.html'
    def get_queryset(self):
        return self.model.objects.order_by('steel_class')

class Steel(ContextMixin, DetailView):
    model = Metal_info
    template_name = 'metal/steel-slug.html'
    context_object_name = "metal_info"

class Steel_class_slug(ContextMixin, SingleObjectMixin, ListView):
    template_name = 'metal/steel-steel_class-slug.html'
    paginate_by = 8
    paginate_orphans =2
    slug_model = Metal_class
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.slug_model.__name__.lower()] = self.object #определяем имя, оно используется в шаблоне
        return context

    def get(self, request, *args, **kwargs):
        # queryset для автоматического поиска. Явно указываем queryset что искал там там где надо.
        # .get_object можно переопределять для ручного поиска
        self.object = self.get_object(queryset=self.slug_model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.metals_info.all() # здесь выбирается кверисет , который будет page_obj

class SearchAll(ContextMixin, ListView):
    paginate_by = 20
    paginate_orphans =5
    model = MetalSearch
    template_name = 'metal/steel-result.html'
    def get_queryset(self):
        return self.model.count_manager.order_by('-date')