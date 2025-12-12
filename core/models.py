from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CLIENTE = "cliente"
    ROLE_FUNCIONARIO = "funcionario"

    ROLE_CHOICES = [
        (ROLE_CLIENTE, "Cliente"),
        (ROLE_FUNCIONARIO, "Funcionário"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Cliente")

    cpf_cnpj = models.CharField(max_length=200, unique=True)
    telefone = models.CharField(max_length=15)
    logradouro = models.CharField(max_length=200)
    cep = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.username} ({self.email})"