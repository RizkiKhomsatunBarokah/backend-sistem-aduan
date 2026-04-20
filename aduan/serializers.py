from rest_framework import serializers
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