from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, InstansiViewSet

router = DefaultRouter()
router.register(r'instansi', InstansiViewSet, basename='instansi')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]