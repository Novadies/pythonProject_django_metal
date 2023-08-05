
from django.http import request
from django.shortcuts import render
from django.views.generic import View

from .utils import *
from .forms import *
from .tools import *  #не удалять, its work

class Start(NoSlugMixin, View):
    models = [Metal_info]
    data = models[0].objects.all()
    Qset = [data]
    #to_padinator = (data, '20')
    Data = dict(zip(models, Qset ))
    template = 'metal/start.html'


class Search(NoSlugMixin, View):
    models = [Metal, Metal_info, Metal_class]
    data2 = models[1].objects.all()
    data3 = models[2].objects.all()
    Qset = [data2, data3]
    Data = dict(zip(models[1:], Qset))
    dict_dop = {models[0].__name__.lower(): models[0].field_S('Fe')}
    form = MetalForm()
    dict_dop.update({'form' : form})
    template = 'metal/search.html'
    def post(self, request):
        bound_form=MetalForm(request.POST)
        if bound_form.is_valid():
            pass
        return render(request, self.template, context={'form' : bound_form})

class Steel_class(NoSlugMixin, View):
    models = [Metal_class]
    data = models[0].objects.all()
    Qset = [data]
    Data = dict(zip(models, Qset))
    template = 'metal/steel_class.html'

class Steel(ForSlugMixin, View):
    model = Metal_info
    template = 'metal/steel_slug.html'

class Steel_class_slug(ForSlugMixin, View):
    model = Metal_class
    template = 'metal/steel_class_slug.html'