from django.db import models
from django.db.models import Count
class CountManager(models.Manager):
    _name = "total"

    def __init__(self, to_annotate, name=_name, ordering=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_annotate = to_annotate
        self.name = name
        self.ordering = "-" if not ordering else ""

    def get_queryset(self):
        in_annotate = {self.name: Count(self.to_annotate)}  # счётчик
        return (
            super()
            .get_queryset()
            .annotate(**in_annotate)
            .order_by(self.ordering + self.name)
        )