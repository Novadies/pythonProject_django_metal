from django.urls import path
from .views import *

urlpatterns = [
    path('start/', NewStart.as_view(), name='start-url'),
    path('search/', NewSearch.as_view(), name='search-url'),
    path('search/<slug:slug>/', NewSearch.as_view(), name='search-slug-url'),
    path('steel/steel_class/', Steel_class.as_view(), name='steel-steel_class-url'),
    path('steel/steel_class/<slug:slug>/', Steel_class_slug.as_view(), name='steel-steel_class-slug-url'),
    path('steel/result/', SearchAll.as_view(), name='steel-result-url'),
    path('steel/<slug:slug>/', Steel.as_view(), name='steel-slug-url'),
    # path('steel/function/<str:slug>/', Function_index.as_view(), name='function_index_url'),
    #path('upload_csv/', upload_csv, name='upload_csv'),     # для загрузки файлов
]
