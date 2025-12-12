from django.urls import path
from .views import *

urlpatterns = [
    path('registros/', py_OrdemdeServico, name="os"),
    path('registros/<int:id_ordem>', py_OrdemdeServico, name="Ordem_detalhes"),
    # Rotas para o CRUD de pratos
    path('cria-ordem', ordemservico_pyCriar, name='cria_ordem'),
    path('deleta/<int:id_ordem>', py_delete_OrdemdeServico, name='deleta_ordem'),
    path('atualiza/<int:id_ordem>', py_edita_OrdemdeServico, name='edita_ordem'),
]