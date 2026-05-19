from django.urls import path
from .views import create_laporan

urlpatterns = [
    path('laporan/', create_laporan),
]