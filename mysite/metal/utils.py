from django.shortcuts import get_object_or_404, get_list_or_404, render


class ObjiectDetailMixin():
    models=[]
    Qset = []
    template= None
    dict2 ={}
    def get(self, requests, slug=None):
        dict1={model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()}
        context={**dict1,**self.dict2}
        return render(requests, self.template, context=context)
