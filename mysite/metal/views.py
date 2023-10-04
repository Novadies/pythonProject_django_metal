from django.urls import reverse_lazy
from django.views.generic import View, ListView, FormView, CreateView
from django.views.generic.list import MultipleObjectMixin
from django.utils.timezone import make_aware

from .forms import *
from .utils import *
from .tools import *


menu = {'metal/start.html':'Обзор сплавов',
        'metal/search.html':'Поиск сплавов',
        'metal/steel_class.html': 'Виды применения стали',
        'metal/steel_slug.html': 'Сталь',
        'metal/steel_class_slug.html': 'Вид применения стали',
        }
class Start(NoSlugMixin, If_paginator, View):
    models = [Metal_info]
    to_padinator = (models[0].objects.all(), '20')
    template = 'metal/start.html'
    dict_dop = {'menu': menu[template]}

class Search(NoSlugMixin, View):
    models = [Metal, Metal_info]
    models_for_data = models[1:]
    Qset = [models.objects.all() for models in models_for_data]
    if Qset: Data = dict(zip(models_for_data, Qset))
    dict_dop = {models[0].__name__.lower(): models[0].field_S('Fe')}

    form = MetalForm
    dict_dop.update({'form': form})
    template = 'metal/search.html'
    def post(self, request):
        bound_form=MetalForm(request.POST)
        if bound_form.is_valid():
            pass
        return render(request, self.template, context={'form': bound_form})

class NewSearch(FormView):   # CreateView сохраняет автоматически, это хорошо если не переопределяется form_valid
    template_name = 'metal/search.html'
    form_class = MetalForm
    success_url = reverse_lazy('search-url')
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu[self.template_name]
        return context

    # def get_success_url(self):
    #
    #     return reverse_lazy('search-slug-url', args=[self.get_dop_field()[1]])

    def get_dop_field(self):
        date = make_aware(datetime.now())
        slug = str(date)[-21:-6].replace(':', '+').replace('.', '-')
        return date, slug
    # @staticmethod
    # def search_for_connections():
    #     return MetalForm.search_for_connections(MetalForm)
    def form_valid(self, form):
        dop_field={'slug':self.get_dop_field()[1], 'date':self.get_dop_field()[0]}
        # добавляем данные с формы, а так же сгенерированые самостоятельно
        for_save_to_db = self.form_class.Meta.model.objects.create(**dop_field, **form.cleaned_data)
        for i in self.form_class.search_for_connections(form.cleaned_data): # добавление связей
            for_save_to_db.metals_info.add(i)
        for_save_to_db.save()
        return super().form_valid(form)

class NewSearchRedirect(NewSearch, MultipleObjectMixin):
    paginate_by = 10
    paginate_orphans = 5
    # def get_context_data(self, *, object_list=None, **kwargs):

    #     return context
    #def get_queryset(self):
        #return Metal_class.objects.order_by('steel_class')


class Steel_class(ListView):
    paginate_by = 10
    paginate_orphans =5
    # model = Metal_class
    # context_object_name = model.__name__.lower()
    template_name = 'metal/steel_class.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu[self.template_name]
        return context
    def get_queryset(self):
        return Metal_class.objects.order_by('steel_class')

class Steel(ForSlugMixin, View):
    model = Metal_info
    template = 'metal/steel_slug.html'
    dict_dop = {'menu': menu[template]}

class Steel_class_slug(ForSlugMixin, View):
    model = Metal_class
    template = 'metal/steel_class_slug.html'
    dict_dop = {'menu': menu[template]}

