import uuid
from django.db import models

class User(models.Model):
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    no_hp = models.CharField(max_length=15)
    
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('instansi', 'instansi')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.nama
    

class Instansi(models.Model):
    id_instansi = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_instansi = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15)
    jenis_instansi = models.CharField(max_length=50)
    alamat = models.CharField(max_length=100)


class Laporan(models.Model):
    id_laporan = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instansi_id = models.ForeignKey(Instansi, on_delete=models.CASCADE)
    
    foto = models.CharField(max_length=100)
    tgl_laporan = models.DateTimeField()  # disesuaikan ke database
    
    deskripsi = models.TextField()  # typo diperbaiki

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.kategori} - {self.id_laporan}"