from django.urls import path
from .views import *
from .views_for_csv import upload_csv

urlpatterns = [
    path('', Start_page.as_view(), name='start_page_url'),
    path('steel/<str:slug>/', Post_index.as_view(), name='post_index_url'),
    path('upload_csv/', upload_csv, name='upload_csv'),     # для загрузки файлов
]
