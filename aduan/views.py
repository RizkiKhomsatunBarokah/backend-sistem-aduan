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