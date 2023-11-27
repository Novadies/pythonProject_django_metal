import django_filters
from .models import Metal_info, Metal_2

class Metal_infoFilter(django_filters.FilterSet):
    def __init__(self, data, *args, **kwargs): # если используются связанные модели необходимо переопределять __init__
        data = data.copy() if data is not None else {} # значения без self доступны только внутри функции
        data.setdefault('metals_class__steel_class', 'По данным сталям нет информации') # можно установить начальные значения, например
        super().__init__(data, *args, **kwargs)
    #   self.queryset = self.Meta.model.objects.select_related("metals_class") # можно переопределить кверисет

    steel = django_filters.CharFilter(lookup_expr='icontains')
    steel_info = django_filters.CharFilter(lookup_expr='icontains')
    metals_class__steel_class = django_filters.AllValuesFilter()
    class Meta:
        model = Metal_info
        exclude = [field.name for field in model._meta.fields+model._meta.many_to_many]

    @property
    def qs(self): # если не переопределять init
        queryset = super().qs
        return queryset.select_related("metals_class")



# class Metal_2Filter(django_filters.FilterSet):
#     title = django_filters.CharFilter(lookup_expr='icontains', label='Title contains')
#     author = django_filters.CharFilter(lookup_expr='icontains', label='Author contains')
#     genre = django_filters.CharFilter(lookup_expr='icontains', label='Genre contains')
#     publication_year = django_filters.NumberFilter(label='Publication Year')
#
#     class Meta:
#         model = Metal_2
#         fields = ['']
