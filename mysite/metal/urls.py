from django.urls import path
from .views import *
from .views_for_csv import upload_csv

urlpatterns = [
    path('start/', Start.as_view(), name='start-url'),
    path('search/', NewSearch.as_view(), name='search-url'),
    path('search/<slug:slug>/', NewSearchRedirect.as_view(), name='search-slug-url'),
    path('steel/steel_class/', Steel_class.as_view(), name='steel-steel_class-url'),
    path('steel/steel_class/<slug:slug>/', Steel_class_slug.as_view(), name='steel-steel_class-slug-url'),
    path('steel/<slug:slug>/', Steel.as_view(), name='steel-slug-url'),
    # path('steel/function/<str:slug>/', Function_index.as_view(), name='function_index_url'),
    # path('upload_csv/', upload_csv, name='upload_csv'),     # для загрузки файлов
]
