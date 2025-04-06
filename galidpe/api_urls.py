# chemin : dpe/api_urls.py

from django.urls import include, path

urlpatterns = [
    path('v1/galidpe/', include('galidpe.api.v1.urls')),
]