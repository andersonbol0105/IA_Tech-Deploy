# cliente/serializers.py
from rest_framework import serializers
from .models import Cliente
from core.models import User
from core.serializers import UserSerializer


class ClienteCreateSerializer(serializers.Serializer):
    # Dados do usuário
    username = serializers.CharField(required=True) 
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    cpf_cnpj = serializers.CharField(required=True)
    telefone = serializers.CharField(required=True)
    logradouro = serializers.CharField(required=True)
    cep = serializers.CharField(required=True)
    cidade = serializers.CharField(required=True)
    estado = serializers.CharField(required=True)

    # Dados do cliente
    empresa = serializers.CharField(required=True)
    setor = serializers.CharField(required=True)


class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ["id", "empresa", "setor", "user"]
