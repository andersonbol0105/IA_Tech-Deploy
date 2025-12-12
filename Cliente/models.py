from django.db import models
from core.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente", default=1)
    empresa = models.CharField(max_length=50)
    setor = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user} {self.empresa} {self.setor}'