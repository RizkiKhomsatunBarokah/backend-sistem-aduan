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
from .models import User, Instansi

class InstansiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instansi
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    instansi = serializers.PrimaryKeyRelatedField(
        queryset=Instansi.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'nama', 'no_hp', 'role', 'instansi']
    def create(self, validated_data):
        instansi_data = validated_data.pop('instansi', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nama=validated_data['nama'],
            no_hp=validated_data.get('no_hp', ''),
            role=validated_data.get('role', 'instansi'),
            instansi_id=instansi_data
        )
        return user
