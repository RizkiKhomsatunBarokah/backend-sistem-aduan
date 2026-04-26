from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
import uuid
from .models import User
from django.core.mail import send_mail
from django.conf import settings

reset_tokens = {}

@api_view(['POST'])
def request_reset_password(request):
    email = request.data.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'User tidak ditemukan'}, status=404)

    token = str(uuid.uuid4())
    reset_tokens[token] = user.id_user

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    send_mail(
        'Reset Password',
        f'Klik link ini: {reset_link}',
        settings.EMAIL_HOST_USER,  # Pakai ini agar otomatis ambil 'muhammadrifai3776@gmail.com'
        [email],
        fail_silently=False,
    )

    return Response({'message': 'Email reset dikirim'})

@api_view(['POST'])
def confirm_reset_password(request):
    token = request.data.get('token')
    password = request.data.get('password')

    if token not in reset_tokens:
        return Response({'message': 'Token tidak valid'}, status=400)

    user_id = reset_tokens[token]
    user = User.objects.get(id_user=user_id)

    user.password = make_password(password)
    user.save()

    del reset_tokens[token]

    return Response({'message': 'Password berhasil direset'})