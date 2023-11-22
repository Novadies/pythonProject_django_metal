"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from . import settings
from .views import pagenotfound

urlpatterns = [
    #path('', Start_page.as_view(), name='start_page_url'),
    path('admin/', admin.site.urls),
    path('metal/', include('metal.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
]
handler404 = pagenotfound
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Список приложений"

if settings.DEBUG:
    try:
        import debug_toolbar
    except Exception: pass

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


