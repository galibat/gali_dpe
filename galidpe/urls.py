# chemin : dpe/urls.py

from django.urls import path
from .views import *

app_name = 'galidpe'

urlpatterns = [
    path("galidpe_list/", dpe_list_view, name="galidpe_list"),
    path("galidpe_analyse/<str:ademe>/", dpe_analyse_view, name="galidpe_analyse"),
    path("galidpe_analyse_export_pdf/<str:ademe>/", dpe_analyse_export_pdf, name="galidpe_analyse_export_pdf"),
    
]
