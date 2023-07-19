from django.views.generic import View
from .utils import ObjiectDetailMixin

from .models import *
#from .qwe import *   # заполнение базы данных!!!!

class Start_page(ObjiectDetailMixin, View):
    model = Metal
    template = 'metal/index.html'


class Post_index(ObjiectDetailMixin, View):
    model = Metal_info
    template = 'metal/post_index.html'
