from django.urls import path
from .views import *

urlpatterns = [
    path('registros/', py_obter_equipamento, name="equipamento"),
    path('registros/<int:id_equipamento>', py_obter_equipamento, name="equipamento_detalhe"),

    # Rotas para o CRUD de Equipamentos 
    path('cria-equipamento', py_cria_equipamento, name='cria_equipamento'),
    path('deleta/<int:id_equipamento>', py_deleta_equipamento, name='deleta_equipamento'),
    path('atualiza/<int:id_equipamento>', py_edita_equipamento, name='edita_equipamento'),
]

