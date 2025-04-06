# chemin : dpe/api_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from galidpe.utils.dpe_db_json import dpe_db_to_json
from galidpe.utils.dpe_analyse import DPEMoteurAnalyse

@extend_schema(
    summary="Récupère un DPE en JSON à partir du numéro ADEME",
    description="Cette API retourne un DPE complet au format JSON2 à partir du numéro ADEME fourni dans l'URL.",
    parameters=[
        OpenApiParameter(name='ademe', description="Numéro ADEME à 13 chiffres", required=True, type=str),
    ],
    responses={
        200: OpenApiResponse(description="DPE trouvé, contenu JSON2 retourné"),
        404: OpenApiResponse(description="DPE introuvable"),
    }
)
class DpeJsonByAdemeView(APIView):
    def get(self, request, ademe):
        try:
            json2_content = dpe_db_to_json(ademe)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(json2_content, status=status.HTTP_200_OK)



@extend_schema(
    summary="Exécute l'analyse d'un DPE à partir de son numéro ADEME",
    description="Cette API retourne le résultat d'analyse d'un DPE, après traitement complet par le moteur d'analyse.",
    parameters=[
        OpenApiParameter(name='ademe', description="Numéro ADEME à 13 chiffres", required=True, type=str),
    ],
    responses={
        200: OpenApiResponse(description="Analyse effectuée avec succès, résultat JSON retourné"),
        404: OpenApiResponse(description="DPE introuvable ou erreur d'analyse"),
    }
)
class DpeAnalyseByAdemeView(APIView):
    def get(self, request, ademe):
        try:
            json2_content = dpe_db_to_json(ademe)
            dpe = DPEMoteurAnalyse(json2_content, ademe=ademe)
            dpe.execute_analyse()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(dpe.to_dict(), status=status.HTTP_200_OK)
    