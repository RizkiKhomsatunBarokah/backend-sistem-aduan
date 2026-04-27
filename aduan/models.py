import uuid
from django.db import models

class User(models.Model):
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    no_hp = models.CharField(max_length=15)
    ROLE_CHOICES=[
        ('admin', 'admin'),
        ('instansi','instansi')
    ]
    role = models.CharField(choices=ROLE_CHOICES)

    def __str__(self):
        return self.nama
    
class Instansi(models.Model):
    id_instansi =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id =models.ForeignKey(User, on_delete=models.CASCADE, related_name='user' )
    nama_instansi =models.CharField(max_length=100)
    no_telp =models.CharField(max_length=15)
    jenis_instansi =models.CharField(max_length=50)
    alamat =models.CharField(max_length=100)

class Laporan(models.Model):
    id_laporan =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instansi_id =models.ForeignKey(Instansi, on_delete=models.CASCADE, related_name='instansi')
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
    
    nama_pelapor = models.CharField(max_length=100)
    no_hp_pelapor = models.CharField(max_length=15)
    email_pelapor = models.EmailField(blank=True, null=True)


    def __str__(self):
        return f"{self.kategori} - {self.nama_pelapor}"


