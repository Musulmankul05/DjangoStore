from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("", include("store.urls")),
                  path("", include("users.urls")),
                  path("orders/", include("orders.urls")),
                  path("accounts/", include("allauth.urls")),
              ] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
