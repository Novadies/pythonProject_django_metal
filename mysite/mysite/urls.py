from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

from . import settings
from .views import redirect_page, decorator_redirect_page

urlpatterns = [
    path('', decorator_redirect_page('search-url')(redirect_page)),
    path('admin/', admin.site.urls),
    path('metal/', include('metal.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('users/', include('allauth.urls')),
    #path('pages/', include('django.contrib.flatpages.urls')),
    #path('silk/', include('silk.urls', namespace='silk')),
]

handler404 = 'mysite.views.pagenotfound'

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Список приложений"

from icecream import install

install()
ic.configureOutput(includeContext=True)  # указание строки и места выполнения

if settings.DEBUG:

    try:
        import debug_toolbar
    except Exception: pass

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


