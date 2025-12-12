# cliente/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction

from .models import Cliente
from .serializers import ClienteSerializer, ClienteCreateSerializer
from core.models import User


class ClienteCreateView(generics.CreateAPIView):
    """
    Rota aberta para criar um cliente (e automaticamente um User).
    """
    permission_classes = [AllowAny]
    serializer_class = ClienteCreateSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ClienteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Criando usuário
        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data.get("email", ""),
            password=serializer.validated_data["password"],
            cpf_cnpj=serializer.validated_data["cpf_cnpj"],
            telefone=serializer.validated_data["telefone"],
            logradouro=serializer.validated_data["logradouro"],
            cep=serializer.validated_data["cep"],
            cidade=serializer.validated_data["cidade"],
            estado=serializer.validated_data["estado"],
        )

        # Criando cliente vinculado
        cliente = Cliente.objects.create(
            user=user,
            empresa=serializer.validated_data["empresa"],
            setor=serializer.validated_data["setor"],
        )

        return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)


class ClienteListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return Cliente.objects.filter(user__is_active=True)


class ClienteDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.filter(user__is_active=True)


class ClienteUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteCreateSerializer  

    def get_queryset(self):
        return Cliente.objects.filter(user__is_active=True)


class ClienteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cliente.objects.all()

    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()
        cliente.user.is_active = False
        cliente.user.save()
        return Response({"detail": "Cliente desativado."}, status=status.HTTP_204_NO_CONTENT)
