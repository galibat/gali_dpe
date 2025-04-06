# views.py
from django.shortcuts import render
from django.shortcuts import redirect


def mainpage_view(request):
    return render(request, "home/mainpage.html")

import markdown
from pathlib import Path
from django.shortcuts import render
from django.http import Http404

def license_view(request):
    license_path = Path(__file__).resolve().parent.parent / "LICENSE.md"
    if not license_path.exists():
        raise Http404("Fichier LICENSE.md introuvable.")

    with open(license_path, encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=["extra", "toc", "tables"])
    return render(request, "home/license.html", {"license_html": html_content})
