from django.urls import path
from .views import create_laporan
from .views import request_reset_password, confirm_reset_password
from rest_framework.routers import DefaultRouter
from .views import RegisterView, InstansiViewSet
from .views import login, RegisterView, InstansiViewSet, predict_aduan

router = DefaultRouter()
router.register(r'instansi', InstansiViewSet, basename='instansi')

urlpatterns = [
    path('laporan/', create_laporan),
    path('reset-password/', request_reset_password),
    path('reset-password-confirm/', confirm_reset_password),
     path('register/', RegisterView.as_view(), name='register'),
      path('login/', login),
      path('predict/', predict_aduan, name='predict-aduan'),
    
]