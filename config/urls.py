import debug_toolbar

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings

from mainapp.apps import MainappConfig

urlpatterns = [
    path("", RedirectView.as_view(url='mainapp/')),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("mainapp/", include("mainapp.urls", namespace=MainappConfig.name)),
    path("authapp/", include("authapp.urls", namespace="authapp")),
    path("social_auth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)