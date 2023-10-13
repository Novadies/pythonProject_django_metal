
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.views.generic import View, ListView, FormView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.utils.timezone import make_aware


from .forms import *
from .tools.decorators2 import track_queries
from .utils import *


class Start(NoSlugMixin, If_paginator, View):
    models = [Metal_info]
    to_padinator = (models[0].objects.all(), '20')
    template = 'metal/start.html'
    dict_dop = {'menu': menu[template]}

class NewSearch(View):
    def get(self, request, *args, **kwargs):
        view = GetSearch.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostSearch.as_view()
        return view(request, *args, **kwargs)

class GetSearch(SearchMixin, ContextMixin, SingleObjectMixin, ListView):
    paginate_by = 10
    paginate_orphans = 5
    form_class = MetalForm
    slug_model = form_class.Meta.model
    def get_paginate_by(self, queryset):
        if self.kwargs:
            return self.paginate_by

    def get_initial(self):
        return self.get_object(queryset=self.slug_model.objects.all()) if self.kwargs else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['initial'] = {field: getattr(self.object, field, None) for field in self.form_class.Meta.fields}
        context['form'] = self.form_class(extra_data=context['initial'])
        context[self.slug_model.__name__.lower()] = self.object
        return context

    def get_queryset(self):
        if self.object:
            return self.object.metals_info.all() # здесь выбирается кверисет , который будет page_obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_initial()
        return super().get(request, *args, **kwargs)


class PostSearch(SearchMixin, CreateView):
    def get_dop_field(self):
        date = make_aware(datetime.now())
        slug = str(date)[-21:-6].replace(':', '_').replace('.', '-')
        return date, slug

    @track_queries
    def form_valid(self, form):
        dop_field={'slug': self.get_dop_field()[1], 'date': self.get_dop_field()[0]}
        # добавляем данные с формы, а так же сгенерированые самостоятельно
        for_save_to_db = self.form_class.Meta.model.objects.create(**dop_field, **form.cleaned_data)
        connections = self.form_class.search_for_connections(form.cleaned_data)
        for_save_to_db.metals_info.add(*connections)
        return HttpResponseRedirect(reverse('search-slug-url', args=[dop_field['slug']]))


class Steel_class(ContextMixin, ListView):
    paginate_by = 10
    paginate_orphans =5
    model = Metal_class
    template_name = 'metal/steel-steel_class.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return self.model.objects.order_by('steel_class')

class Steel(ContextMixin, DetailView):
    model = Metal_info
    template_name = 'metal/steel-slug.html'
    context_object_name = "metal_info"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Steel_class_slug(ContextMixin, SingleObjectMixin, ListView):
    template_name = 'metal/steel-steel_class-slug.html'
    paginate_by = 8
    paginate_orphans =2
    slug_model = Metal_class
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.slug_model.__name__.lower()] = self.object
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return self.model.objects.order_by('-date')