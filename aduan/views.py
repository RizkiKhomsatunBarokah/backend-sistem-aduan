from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoginSerializer

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        return Response({
            'status': 'success',
            'message': 'Login berhasil',
            'data': {
                'id_user': str(user.id_user),
                'nama': user.nama,
                'role': user.role
            }
        })

    return Response({
        'status': 'error',
        'message': serializer.errors
    }, status=400)
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
