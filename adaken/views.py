from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class SampleAPIView(APIView):

    def get(self, request):
        return Response("OK", status=status.HTTP_200_OK)
