from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login, RegisterView, InstansiViewSet

router = DefaultRouter()
router.register(r'instansi', InstansiViewSet, basename='instansi')

urlpatterns = [
    path('login/', login),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]