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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Laporan, Instansi
import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Instansi
from .serializers import RegisterSerializer, InstansiSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # Pastikan sudah install djangorestframework-simplejwt
from .serializers import LoginSerializer, RegisterSerializer, InstansiSerializer
from .models import Instansi
import joblib
import os

reset_tokens = {}

# Load model ML sekali saja saat server berjalan agar cepat
MODEL_PATH = os.path.join(settings.BASE_DIR, 'aduan', 'ml_models', 'model_klasifikasi.pkl')

try:
    ml_model = joblib.load(MODEL_PATH)
except Exception as e:
    ml_model = None
    print(f"Gagal memuat model ML: {str(e)}")

@api_view(['POST'])
def predict_aduan(request):
    if ml_model is None:
        return Response({'error': 'Model Machine Learning tidak tersedia di server'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # 1. Ambil data input/fitur dari Postman atau Frontend
    # Contoh: jika model menerima teks deskripsi untuk mendeteksi ODGJ/PGOT secara otomatis
    deskripsi_teks = request.data.get('deskripsi')
    
    if not deskripsi_teks:
        return Response({'error': 'Input deskripsi aduan wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # 2. Lakukan pemrosesan teks atau ekstraksi fitur sesuai kebutuhan modelmu
        # Contoh sederhana (sesuaikan dengan cara modelmu menerima input):
        input_data = [deskripsi_teks] 
        
        # 3. Lakukan Prediksi
        prediksi = ml_model.predict(input_data)
        hasil_kategori = prediksi[0] # Misalnya return string 'ODGJ' atau 'PGOT'
        
        # 4. Kembalikan jawaban ke Postman/Frontend
        return Response({
            'status': 'success',
            'input_deskripsi': deskripsi_teks,
            'rekomendasi_kategori_ml': hasil_kategori
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': f'Gagal melakukan prediksi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

@csrf_exempt
def create_laporan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # Karena kita pakai form-data di Postman/Frontend
        kategori = request.POST.get('kategori')
        deskripsi = request.POST.get('deskripsi')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        foto_file = request.FILES.get('foto') 
        nama_pelapor = request.POST.get('nama_pelapor') or "Warga"
        email_pelapor = request.POST.get('email_pelapor') or "masyarakat@email.com"
        no_hp_pelapor = request.POST.get('no_hp_pelapor') or "-"
        hubungan_pelapor = request.POST.get('hubungan_pelapor') or "Warga"

        if not deskripsi:
            return JsonResponse({'error': 'Detail aduan wajib diisi'}, status=400)

        instansi = Instansi.objects.first()
        if not instansi:
            return JsonResponse({'error': 'Instansi kosong'}, status=500)

        # Simpan ke Database
        laporan = Laporan.objects.create(
            instansi_id=instansi,
            kategori=kategori if kategori in ['ODGJ', 'PGOT'] else 'ODGJ',
            deskripsi=deskripsi,
            latitude=float(latitude) if latitude else 0.0,
            longitude=float(longitude) if longitude else 0.0,
            foto=foto_file.name if foto_file else "default.jpg",
            tgl_laporan=timezone.now(),
            status='menunggu',
            nama_pelapor=request.POST.get('nama_pelapor'),
            email_pelapor=request.POST.get('email_pelapor'),
            no_hp_pelapor=request.POST.get('no_hp_pelapor'),
            hubungan_pelapor=request.POST.get('hubungan_pelapor')
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Laporan berhasil dikirim',
            'id_laporan': str(laporan.id_laporan)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
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