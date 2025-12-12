from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from core.models import User
from .models import Funcionario
from .serializers import FuncionarioSerializer, FuncionarioCreateSerializer


class FuncionarioCreateView(generics.CreateAPIView):
    """
    Somente administradores podem criar funcionários.
    """
    serializer_class = FuncionarioCreateSerializer
    permission_classes = [IsAdminUser]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = FuncionarioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Criar usuário base
        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            first_name=data["first_name"],
            email=data["email"],
            cpf_cnpj=data["cpf_cnpj"],
            telefone=data["telefone"],
            logradouro=data["logradouro"],
            cep=data["cep"],
            cidade=data["cidade"],
            estado=data["estado"],
        )

        # Funcionário sempre é staff
        user.is_staff = True
        user.save()

        funcionario = Funcionario.objects.create(
            user=user,
            especialidade=data["especialidade"],
            cargo=data["cargo"],
            salario=data["salario"]
        )

        return Response(FuncionarioSerializer(funcionario).data, status=status.HTTP_201_CREATED)


class FuncionarioListView(generics.ListAPIView):
    """
    Lista apenas funcionários com usuário ativo.
    """
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Funcionario.objects.filter(user__is_active=True)


class FuncionarioDetailView(generics.RetrieveAPIView):
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    queryset = Funcionario.objects.filter(user__is_active=True)


class FuncionarioUpdateView(generics.UpdateAPIView):
    """
    Atualiza informações do funcionário.
    Dados de usuário também podem ser atualizados.
    """
    serializer_class = FuncionarioCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Funcionario.objects.filter(user__is_active=True)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        funcionario = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Atualizar USER
        user = funcionario.user
        user.first_name = data["first_name"]
        user.email = data["email"]
        user.telefone = data["telefone"]
        user.logradouro = data["logradouro"]
        user.cep = data["cep"]
        user.cidade = data["cidade"]
        user.estado = data["estado"]

        # Funcionário deve continuar staff
        user.is_staff = True
        user.save()

        # Atualizar funcionario
        funcionario.especialidade = data["especialidade"]
        funcionario.cargo = data["cargo"]
        funcionario.salario = data["salario"]
        funcionario.save()

        return Response(FuncionarioSerializer(funcionario).data)


class FuncionarioDeleteView(generics.DestroyAPIView):
    """
    DELETE apenas desativa o usuário.
    """
    queryset = Funcionario.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        funcionario = self.get_object()
        funcionario.user.is_active = False
        funcionario.user.save()
        return Response({"detail": "Funcionário desativado."}, status=204)
