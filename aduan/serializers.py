from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'nama', 'email', 'no_hp', 'role']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User tidak ditemukan")

        if password != user.password:
            raise serializers.ValidationError("Password salah")

        if user.role not in ['admin', 'instansi']:
            raise serializers.ValidationError("Role tidak diizinkan login")

        # simpan user biar bisa dipakai di views
        data['user'] = user
        return data