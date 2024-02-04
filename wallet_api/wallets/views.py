from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def get_status_view(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
