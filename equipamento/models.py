from django.db import models

# Create your models here.
class Equipamento(models.Model):
    modelo_marca = models.CharField('Modelo e Marca', max_length=50)
    patrimonio = models.CharField('Patrimonio', max_length=50)
    num_serie = models.CharField('Número de Série', max_length=50)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.modelo_marca} {self.patrimonio} | {self.num_serie}'
    

    