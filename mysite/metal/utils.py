from django.shortcuts import get_object_or_404, get_list_or_404, render


class TwoStrMixin():  # тут нет смысла передавать больше чем одну модель во View, но да ладно
    models=[]
    Qset = []
    template= None
    dict2 ={}
    def get(self, request):
        dict1={model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()}
        context={**dict1,**self.dict2}
        return render(request, self.template, context=context)

class ForSlugMixin():  # тут нет смысла передавать больше чем одну модель во View, но да ладно
    model=None
    template= None
    def get(self, request, slug):
        context={self.model.__name__.lower(): get_object_or_404(self.model, slug__iexact=slug)}
        return render(request, self.template, context=context)