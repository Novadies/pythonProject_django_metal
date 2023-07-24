from django.views.generic import View
from .utils import ObjiectDetailMixin
import csv
from .models import *

# Metal.objects.all().delete()
# Metal_info.objects.all().delete()
# Metal_class.objects.all().delete()

START_DB=False
if START_DB:
    from .csv_to_bd import zapis
    with open('metal\sourse\metal.csv') as f:
        reader = csv.DictReader(f, delimiter=';')
        zapis(reader)

############################################################################3

class Start_page_metal(ObjiectDetailMixin, View):
    models = [Metal_info, Metal_class]
    Qset1 = models[0].objects.all()
    Qset2 = models[1].objects.all()
    Qset = [Qset1, Qset2]
    template = 'metal/start.html'


class Search_index(ObjiectDetailMixin, View):
    models = [Metal, Metal_info, Metal_class]
    Qset1 = models[0].objects.all()
    Qset2 = models[1].objects.all()
    Qset3 = models[2].objects.all()
    Qset = [Qset1, Qset2, Qset3]
    template = 'metal/search.html'
