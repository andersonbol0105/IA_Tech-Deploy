from rest_framework import serializers
from core.models import User
from .models import Funcionario


class FuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializer para listar e detalhar funcionários.
    """
    nome = serializers.CharField(source="user.first_name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    cpf_cnpj = serializers.CharField(source="user.cpf_cnpj", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)  # ADICIONE
    telefone = serializers.CharField(source="user.telefone", read_only=True)  # ADICIONE
    logradouro = serializers.CharField(source="user.logradouro", read_only=True)  # ADICIONE
    cep = serializers.CharField(source="user.cep", read_only=True)  # ADICIONE
    cidade = serializers.CharField(source="user.cidade", read_only=True)  # ADICIONE
    estado = serializers.CharField(source="user.estado", read_only=True)  # ADICIONE

    class Meta:
        model = Funcionario
        fields = [
            "id",
            "nome",
            "email",
            "cpf_cnpj",
            "username",      # ADICIONE
            "telefone",      # ADICIONE
            "logradouro",    # ADICIONE
            "cep",           # ADICIONE
            "cidade",        # ADICIONE
            "estado",        # ADICIONE
            "cargo",
            "especialidade",
            "salario",
            "data_admissao",
        ]
class FuncionarioCreateSerializer(serializers.Serializer):
    """
    Serializer de criação que também cria o usuário automaticamente.
    """

    # Dados do usuário
    username = serializers.CharField(required=True) 
    first_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    cpf_cnpj = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)
    telefone = serializers.CharField(max_length=15)
    logradouro = serializers.CharField(max_length=200)
    cep = serializers.CharField(max_length=10)
    cidade = serializers.CharField(max_length=50)
    estado = serializers.CharField(max_length=2)

    # Dados do funcionário
    especialidade = serializers.CharField(max_length=50)
    cargo = serializers.CharField(max_length=50)
    salario = serializers.DecimalField(max_digits=10, decimal_places=2)


    def validate_cpf_cnpj(self, value):
        if User.objects.filter(cpf_cnpj=value).exists():
            raise serializers.ValidationError("Já existe um usuário com esse CPF/CNPJ.")
        return value
