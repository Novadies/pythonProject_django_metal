from django.urls import path
from .views import *
from .views_for_csv import upload_csv

urlpatterns = [
    path('start/', Start.as_view(), name='start_url'),
    path('search/', Search.as_view(), name='search_url'),
    # path('steel/<int:slug>/', Search_index.as_view(), name='search_index_url'),  # TODO заменитьв models
    # path('steel/mark/<str:slug>/', Mark_index.as_view(), name='mark_index_url'),
    # path('steel/function/<str:slug>/', Function_index.as_view(), name='function_index_url'),
    # path('upload_csv/', upload_csv, name='upload_csv'),     # для загрузки файлов
]
