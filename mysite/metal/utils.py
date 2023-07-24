from django.shortcuts import get_object_or_404, get_list_or_404, render


from .models import *

class ObjiectDetailMixin():
    models=[]
    Qset = []
    template= None
    Data = dict(zip(models, Qset))
    def get(self, requests, slug=None):
        context={self.model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()}
        return render(requests, self.template, context=context)
