from django.urls import path
from .views import request_reset_password, confirm_reset_password

urlpatterns = [
    path('reset-password/', request_reset_password),
    path('reset-password-confirm/', confirm_reset_password),
]