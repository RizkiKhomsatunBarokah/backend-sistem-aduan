from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Laporan, User
import json
from datetime import date


@csrf_exempt
def create_laporan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)

        # ====== STEP 1–3 (inti laporan) ======
        kategori = data.get('kategori')
        deskripsi = data.get('deskripsi')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        foto = data.get('foto')  # sementara string/path/url

        # ====== STEP 4 (DATA PELAPOR - BAGIAN KAMU) ======
        nama = data.get('nama')
        no_hp = data.get('no_hp')
        email = data.get('email')
        hubungan = data.get('hubungan')

        # ====== VALIDASI (minimal tapi penting) ======
        if not kategori:
            return JsonResponse({'error': 'Kategori wajib diisi'}, status=400)

        if not deskripsi:
            return JsonResponse({'error': 'Deskripsi wajib diisi'}, status=400)

        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Lokasi wajib diisi'}, status=400)

        if not nama:
            return JsonResponse({'error': 'Nama pelapor wajib diisi'}, status=400)

        if not no_hp or not str(no_hp).isdigit():
            return JsonResponse({'error': 'No HP tidak valid'}, status=400)

        # format nomor indonesia
        if str(no_hp).startswith("08"):
            no_hp = "+62" + str(no_hp)[1:]

        # ====== INSTANSI (sementara ambil 1 user) ======
        instansi = User.objects.first()  # nanti bisa diganti dari auth / pilihan

        # ====== SIMPAN ======
        laporan = Laporan.objects.create(
            instansi=instansi,
            kategori=kategori,
            deskripsi=deskripsi,
            latitude=latitude,
            longitude=longitude,
            foto=foto,
            tgl_laporan=date.today(),

            # data pelapor
            nama_pelapor=nama,
            no_hp_pelapor=no_hp,
            email_pelapor=email,
            hubungan_pelapor=hubungan
        )

        return JsonResponse({
            'message': 'Laporan berhasil dikirim',
            'id_laporan': str(laporan.id_laporan)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)