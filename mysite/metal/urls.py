from django.urls import path
from .views import *
from .views_for_csv import upload_csv

urlpatterns = [
    path('', Start_page_metal.as_view(), name='start_page_metal_url'),
    path('steel/', Search_index.as_view(), name='search_index_url'),
    # path('steel/<int:slug>/', Search_index.as_view(), name='search_index_url'),
    # path('steel/mark/<str:slug>/', Mark_index.as_view(), name='mark_index_url'),
    # path('steel/function/<str:slug>/', Function_index.as_view(), name='function_index_url'),
    # path('upload_csv/', upload_csv, name='upload_csv'),     # для загрузки файлов
]
