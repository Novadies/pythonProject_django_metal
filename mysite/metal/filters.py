import django_filters
from django.db.models import QuerySet

from .models import Metal_info
import logging

debug_logger = logging.getLogger('debug')


class Metal_infoFilter(django_filters.FilterSet):
    """ фильтр по полям Metal_info """

    def __init__(self, data: dict, *args, **kwargs):
        data = data.copy() if data is not None else {}  # значения без self доступны только внутри функции
        data.setdefault('metals_class__steel_class',
                        'По данным сталям нет информации')  # можно установить начальные значения, например
        super().__init__(data, *args, **kwargs)

    #   self.queryset = self.Meta.model.objects.select_related("metals_class") # можно переопределить кверисет

    steel = django_filters.CharFilter(lookup_expr='icontains')
    steel_info = django_filters.CharFilter(lookup_expr='icontains')
    metals_class__steel_class = django_filters.AllValuesFilter()

    class Meta:
        model = Metal_info
        exclude = [field.name for field in model._meta.fields + model._meta.many_to_many]
        debug_logger.debug(exclude)

    @property
    def qs(self) -> QuerySet:  # если не переопределять init
        """ стандартная функция изменяющая кверисет"""
        queryset = super().qs
        ic(queryset)
        return queryset.select_related("metals_class")
