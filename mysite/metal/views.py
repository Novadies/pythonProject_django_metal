from django.views.generic import View

from .utils import ObjiectDetailMixin
from .models import *
from .forms import *
from .tools import *  #не удалять

class Start(ObjiectDetailMixin, View):
    models = [Metal_info]#, Metal_class]
    Qset1 = models[0].objects.all()
    #Qset2 = models[1].objects.all()
    Qset = [Qset1]#, Qset2]
    Data = dict(zip(models, Qset))
    template = 'metal/start.html'


class Search(ObjiectDetailMixin, View):
    models = [Metal_info, Metal_class]
    Qset2 = models[0].objects.all()
    Qset3 = models[1].objects.all()
    Qset = [Qset2, Qset3]
    Data = dict(zip(models, Qset))
    form = MetalForm()
    dict2 = {Metal.__name__.lower():[field.name for field in Metal._meta.fields][1:-1]} # ни каких идей почему .name работает
    dict2.update({'form' : form})
    template = 'metal/search.html'


