from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/v1/", include("abc_back.api.v1.urls", namespace="v1")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # TODO: используется только в local, возможно стоит переделать или убрать вовсе
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += debug_toolbar_urls()
