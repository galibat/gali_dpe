# chemin : dpe/api_urls.py

from django.urls import include, path

urlpatterns = [
    path('v1/dpe/', include('dpe.api.v1.urls')),
]