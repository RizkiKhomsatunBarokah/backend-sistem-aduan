import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Instansi(models.Model):
    id_instansi =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama_instansi =models.CharField(max_length=100)
    no_telp =models.CharField(max_length=15)
    jenis_instansi =models.CharField(max_length=50)
    alamat =models.CharField(max_length=100)

class User(AbstractUser):
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instansi_id = models.ForeignKey(Instansi, on_delete=models.CASCADE, related_name='instansi')
    nama = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=15)
    ROLE_CHOICES=[
        ('admin', 'admin'),
        ('instansi','instansi')
    ]
    role = models.CharField(choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nama

class Laporan(models.Model):
    id_laporan =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instansi_id =models.ForeignKey(User, on_delete=models.CASCADE, related_name='instansi')
    foto =models.CharField(max_length=100)
    deksripsi =models.TextField()
    KATEGORI_CHOICES = [
        ('ODGJ', 'ODGJ'),
        ('PGOT', 'PGOT')
    ]
    kategori =models.CharField(choices=KATEGORI_CHOICES)
    latitude =models.FloatField(max_length=15)
    longitude =models.FloatField(max_length=15)
    
    STATUS_CHOICES = [
        ('selesai', 'selesai'),
        ('proses', 'proses'),
        ('menunggu', 'menunggu'),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default='menunggu')
    tgl_laporan =models.DateField()


