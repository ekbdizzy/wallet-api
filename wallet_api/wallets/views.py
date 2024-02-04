from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@swagger_auto_schema(tags=['Health check'], methods=["GET", ])
@api_view(["GET"])
def get_status_view(request):
    """Health check view."""
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
