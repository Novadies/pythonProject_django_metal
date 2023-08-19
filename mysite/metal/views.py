from django.views.generic import View

from .utils import *
from .forms import *
from .tools import *  #не удалять, its work

class Start(NoSlugMixin, View):
    models = [Metal_info]
    models_for_data = models
    data = models[0].objects.all()
    to_padinator = (data, '20')
    template = 'metal/start.html'


class Search(NoSlugMixin, View):
    models = [Metal, Metal_info, Metal_class]
    models_for_data = models[1:]
    Qset = [models[1].objects.all(), models[2].objects.all()]
    dict_dop = {models[0].__name__.lower(): models[0].field_S('Fe')}

    form = MetalForm()
    dict_dop.update({'form': form})
    template = 'metal/search.html'
    def post(self, request):
        bound_form=MetalForm(request.POST)
        if bound_form.is_valid():
            pass
        return render(request, self.template, context={'form': bound_form})

class Steel_class(NoSlugMixin, View):
    models = [Metal_class]
    models_for_data = models
    Qset = [models[0].objects.all()]
    template = 'metal/steel_class.html'

class Steel(ForSlugMixin, View):
    model = Metal_info
    template = 'metal/steel_slug.html'

class Steel_class_slug(ForSlugMixin, View):
    model = Metal_class
    template = 'metal/steel_class_slug.html'