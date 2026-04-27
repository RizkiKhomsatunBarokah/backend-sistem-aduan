from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Laporan, Instansi
import json
from django.utils import timezone

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