from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from .models import User, Instansi


# =========================
# USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'nama', 'email', 'no_hp', 'role']


# =========================
# LOGIN SERIALIZER
# =========================
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # cek user berdasarkan email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User tidak ditemukan")

        # 🔥 Cara 1 (pakai check_password)
        if not check_password(password, user.password):
            raise serializers.ValidationError("Password salah")

        # 🔥 Alternatif lebih clean (boleh pakai ini aja)
        # user_auth = authenticate(username=user.username, password=password)
        # if not user_auth:
        #     raise serializers.ValidationError("Password salah")

        # cek role
        if user.role not in ['admin', 'instansi']:
            raise serializers.ValidationError("Role tidak diizinkan login")

        # simpan user ke context
        data['user'] = user
        return data


# =========================
# INSTANSI SERIALIZER
# =========================
class InstansiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instansi
        fields = '__all__'


# =========================
# REGISTER SERIALIZER
# =========================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    instansi = serializers.PrimaryKeyRelatedField(
        queryset=Instansi.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'nama',
            'no_hp',
            'role',
            'instansi'
        ]

    def create(self, validated_data):
        instansi_data = validated_data.pop('instansi', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # otomatis di-hash
            nama=validated_data['nama'],
            no_hp=validated_data.get('no_hp', ''),
            role=validated_data.get('role', 'instansi'),
            instansi_id=instansi_data
        )

        return user