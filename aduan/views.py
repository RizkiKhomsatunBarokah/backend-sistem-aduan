from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # Pastikan sudah install djangorestframework-simplejwt
from .serializers import LoginSerializer, RegisterSerializer, InstansiSerializer
from .models import Instansi

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        # MEMBUAT TOKEN JWT SECARA MANUAL
        refresh = RefreshToken.for_user(user)
        
        # Menyisipkan role ke dalam isi token (payload) 
        # agar bisa dibaca oleh jwt-decode di React
        refresh['role'] = user.role 

        return Response({
            'status': 'success',
            'message': 'Login berhasil',
            'token': str(refresh.access_token), # Ini yang WAJIB ada untuk React
            'data': {
                'id_user': str(user.id_user),
                'nama': user.nama,
                'role': user.role
            }
        })

    return Response({
        'status': 'error',
        'message': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "Berhasil",
                "message": "User berhasil terdaftar"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstansiViewSet(viewsets.ModelViewSet):
    queryset = Instansi.objects.all()
    serializer_class = InstansiSerializer