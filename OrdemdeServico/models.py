from django.db import models
from Cliente.models import Cliente
from funcionario.models import Funcionario
from equipamento.models import Equipamento

# Create your models here.
class OrdemdeServico(models.Model):
    data_de_conclusao = models.DateField(auto_now_add=True)
    status = models.CharField('status', max_length=50)
    data_criacao = models.DateField(auto_now_add=True)
    prioridade = models.CharField('prioridade', max_length=50)
    observacao = models.CharField('observacao', max_length=100)
    diagnostico = models.CharField('diagnostico', max_length=100)
    categoria = models.CharField('categoria', max_length=50)
    problema_relatado = models.CharField('problema_relatado', max_length=100)
    valor_servico = models.CharField('valor_servico', max_length=50 )
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f'{self.status} {self.data_criacao} {self.data_de_conclusao}'