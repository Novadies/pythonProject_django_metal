from django.urls import path
from .views import *

urlpatterns = [
    path('', Start_page.as_view(), name='start_page_url'),
    path('steel/<str:slug>/', Post_index.as_view(), name='post_index_url'),
]
