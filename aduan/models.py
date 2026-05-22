import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class Instansi(models.Model):
    id_instansi =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_instansi =models.CharField(max_length=100)
    no_telp =models.CharField(max_length=15)
    jenis_instansi =models.CharField(max_length=50)
    alamat =models.CharField(max_length=100)

class User(AbstractUser):
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instansi_id = models.ForeignKey(Instansi, on_delete=models.CASCADE, related_name='users')
    nama = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    no_hp = models.CharField(max_length=15, unique=True)

    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('instansi', 'instansi')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.nama


class Laporan(models.Model):
    id_laporan = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    instansi_id = models.ForeignKey(Instansi, on_delete=models.CASCADE)
    nama_pelapor = models.CharField(max_length=100, null=True, blank=True)
    foto = models.CharField(max_length=100)
    tgl_laporan = models.DateTimeField()

    deskripsi = models.TextField()

    KATEGORI_CHOICES = [
        ('ODGJ', 'ODGJ'),
        ('PGOT', 'PGOT')
    ]
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES)

    latitude = models.FloatField()
    longitude = models.FloatField()

    STATUS_CHOICES = [
        ('selesai', 'selesai'),
        ('proses', 'proses'),
        ('menunggu', 'menunggu'),
    ]
    nama_pelapor = models.CharField(max_length=255, null=True, blank=True)
    email_pelapor = models.EmailField(null=True, blank=True)
    no_hp_pelapor = models.CharField(max_length=20, null=True, blank=True)
    hubungan_pelapor = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.kategori} - {self.id_laporan}"