# core/serializers.py
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "cpf_cnpj", "telefone",
            "logradouro", "cep", "cidade", "estado", "is_active"
        ]
        read_only_fields = ["id", "is_active"]
