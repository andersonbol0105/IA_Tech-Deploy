from django.db import models
from core.models import User

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="funcionario", default=1)
    especialidade = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=50)
    data_admissao = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} {self.cargo} {self.especialidade}'
