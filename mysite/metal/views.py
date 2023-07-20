from django.views.generic import View
from .utils import ObjiectDetailMixin
import csv
from .models import *

# Metal.objects.all().delete()
# Metal_info.objects.all().delete()
# Metal_class.objects.all().delete()

START_DB=False
if START_DB:
    from .first_bd import zapis
    with open('metal\sourse\metal.csv') as f:
        reader = csv.DictReader(f, delimiter=';')
        zapis(reader)


class Start_page(ObjiectDetailMixin, View):
    model = Metal
    template = 'metal/index.html'


class Post_index(ObjiectDetailMixin, View):
    model = Metal_info
    template = 'metal/post_index.html'
