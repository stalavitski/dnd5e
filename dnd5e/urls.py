from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', include('characters.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
