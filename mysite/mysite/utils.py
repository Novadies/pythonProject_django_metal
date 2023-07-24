from django.shortcuts import get_object_or_404
from django.shortcuts import render

#from .models import *

class ObjiectDetailMixin():
    model=None
    template= None

    def get(self, requests, slug):
        obj=get_object_or_404(self.model, slug__iexact=slug)
        return render(requests, self.template, context={self.model.__name__.lower():obj})