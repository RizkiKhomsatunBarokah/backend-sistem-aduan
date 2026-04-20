from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Instansi
from .serializers import RegisterSerializer, InstansiSerializer

class InstansiViewSet(viewsets.ModelViewSet):
    queryset=Instansi.objects.all()
    serializer_class = InstansiSerializer

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "Berhasil",
                "message": "User berhasil terdaftar"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)