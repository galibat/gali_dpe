# chemin : dpe/api_urls.py
from django.urls import path
from .views import DpeJsonByAdemeView, DpeAnalyseByAdemeView

urlpatterns = [
    path('dpe_content/ademe/<str:ademe>/', DpeJsonByAdemeView.as_view(), name='api-dpe-content-by-ademe'),
    path('dpe_analyse/ademe/<str:ademe>/', DpeAnalyseByAdemeView.as_view(), name='api-dpe-analyse-by-ademe'),
]