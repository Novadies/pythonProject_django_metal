from django.shortcuts import get_object_or_404, get_list_or_404, render


class NoSlugMixin():  # тут конкретно нет смысла передавать больше чем одну модель во View, но да ладно
    models=[]
    Qset = []
    template= None
    dict2 ={}
    def get(self, request):
        path = {'path_info': request.path_info[:]} # смысла передавать нет, так как в шаблоне доступна непосредственно сам request
        dict1={model.__name__.lower(): get_list_or_404(qset) for model, qset in self.Data.items()} #передаются экземпляры класса
        context={**dict1, **path, **self.dict2}  # передаются дополнительные параметры, например формы
        return render(request, self.template, context=context)

class ForSlugMixin():  # тут нет смысла передавать больше чем одну модель во View, но да ладно
    model=None
    template= None
    def get(self, request, slug):
        context={self.model.__name__.lower(): get_object_or_404(self.model, slug__iexact=slug)} # передаётся экземпляр класса
        return render(request, self.template, context=context)