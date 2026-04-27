from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Laporan, Instansi
import json
from datetime import datetime


@csrf_exempt
def create_laporan(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)

        kategori = data.get('kategori')
        deskripsi = data.get('deskripsi')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        foto = data.get('foto')

        # validasi
        if not kategori:
            return JsonResponse({'error': 'Kategori wajib diisi'}, status=400)

        if not deskripsi:
            return JsonResponse({'error': 'Deskripsi wajib diisi'}, status=400)

        if latitude is None or longitude is None:
            return JsonResponse({'error': 'Lokasi wajib diisi'}, status=400)

        # ambil instansi (sementara)
        instansi = Instansi.objects.first()

        if not instansi:
            return JsonResponse({'error': 'Instansi tidak ditemukan'}, status=400)

        # simpan
        laporan = Laporan.objects.create(
            instansi_id=instansi,
            kategori=kategori,
            deskripsi=deskripsi,
            latitude=latitude,
            longitude=longitude,
            foto=foto,
            tgl_laporan=datetime.now()
        )

        return JsonResponse({
            'message': 'Laporan berhasil dikirim',
            'id_laporan': str(laporan.id_laporan)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)