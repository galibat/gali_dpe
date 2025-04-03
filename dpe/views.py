# chemin : dpe/views.py

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from dpe.models import DpeInfos

from dpe.utils.dpe_xml_json import dpe_file_xml_to_json
from dpe.utils.dpe_db_json import dpe_db_to_json
from dpe.utils.dpe_analyse import DPEMoteurAnalyse
from datetime import datetime

def dpe_list_view(request):
    
    query = request.GET.get("q", "").strip()
    page_number = request.GET.get("page", 1)

    dpeinfos = DpeInfos.objects.select_related("dpe_id").all()

    if query:
        dpeinfos = dpeinfos.filter(
            Q(ademe=query) |
            Q(ug=query) |
            Q(adresse__icontains=query)
        )

    dpeinfos = dpeinfos.order_by("-ademe")

    paginator = Paginator(dpeinfos, 200)
    page_obj = paginator.get_page(page_number)

    return render(request, "dpe/dpe_list.html", {
        "page_obj": page_obj,
        "query": query,
    })
    
def dpe_analyse_view(request, ademe):
    json2_content = dpe_db_to_json(ademe)
    dpe = DPEMoteurAnalyse(json2_content)
    #dpe.add_connaissance("Demandeur", "Demandeur", "Ligne de commande")
    result = dpe.execute_analyse()

    return render(request, "dpe/dpe_analyse.html", {
        "dpe_analyse": dpe.to_dict(),
    })


# dpe/views.py

from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
import json

def dpe_analyse_export_pdf(request, ademe):
    json2_content = dpe_db_to_json(ademe)
    dpe = DPEMoteurAnalyse(json2_content)
    #dpe.add_connaissance("Demandeur", "Demandeur", "Ligne de commande")
    result = dpe.execute_analyse()

    template = get_template("dpe/dpe_analyse_content.html")
    html_string = template.render({
        "dpe_analyse": dpe.to_dict(),
        "is_pdf": False,
    })

    # Génère le PDF depuis le HTML rendu
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    # Utilise un buffer mémoire temporaire
    pdf_file = html.write_pdf()

    # Format du nom : YYYYMMDD_DIAG_DPEANALYSE_<ADEME>.pdf
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}_DIAG_DPEANALYSE_{ademe}.pdf"

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response
