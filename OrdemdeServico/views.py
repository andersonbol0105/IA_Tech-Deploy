from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.utils.dateformat import format
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import OrdemdeServico
# Create your views here.

def _serialize(os):
    return {
        'data_de_conclusao': os.data_conclusao,
        'status': os.status,
        'data_criacao': os.data_criacao,
        'prioridade': os.prioridade,
        'observacao': os.observacao,
        'diagnostico': os.diagnostico,
        'categoria': os.categoria,
        'problema_relatado': os.problema_relatado,
        'valor_servico': os.valor_servico,
        'cliente': os.cliente,
        'equipamento': os.equipamento,
        'funcionario': os.funcionario,
    }  



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ordemservico_pyCriar(request):
    data = request.data
    ordemservico = OrdemdeServico.objects.create(
        data_de_conclusao=data.get('data_de_conclusao'),
        status=data.get('status'),
        data_criacao=data.get('data_criacao'),
        prioridade=data.get('prioridade'),
        observacao=data.get('observacao'),
        diagnostico=data.get('diagnostico'),
        categoria=data.get('categoria'),
        problema_relatado=data.get('problema_relatado'),
        valor_servico=data.get('valor_servico'),
        cliente=data.get('cliente'),
        equipamento=data.get('equipamento'),
        funcionario=request.user #Associa a OS ao usuário logado,
    )
    return Response({'status': 'success', 'id_cliente': ordemservico.id}, status=201)


@api_view(['GET'])
def py_OrdemdeServico(request, id_ordem=None):
    if id_ordem:
        try:
            ordemdeServico = OrdemdeServico.objects.get(pk=id_ordem)
            ordemdeServico_data = _serialize(ordemdeServico)
            return Response({'Ordem': ordemdeServico_data})
        except OrdemdeServico.DoesNotExist:
            return Response({'error': 'Ordem não encontrado.'}, status=404)
    else:
        ordemdeServico = OrdemdeServico.objects.all()
        ordemdeServico_data = [_serialize(ordemdeServico) for ordemdeServico in ordemdeServico]
        return Response({'Ordem': ordemdeServico_data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def py_delete_OrdemdeServico(request, id_ordem):

    ordemdeServico = get_object_or_404(OrdemdeServico, pk=id_ordem, ordemdeServico=request.user)
    ordemdeServico.delete()
    return Response({'status': 'success', 'message': f'Ordem de serviço {id_ordem} deletado com sucesso.'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def py_edita_OrdemdeServico(request, id_ordem):
    ordemdeServico = get_object_or_404(OrdemdeServico, pk=id_ordem)
    data = request.data
    # Atualiza apenas os campos presentes no JSON
    ordemdeServico.status = data.get('Status', ordemdeServico.status)
    ordemdeServico.data_de_conclusao = data.get('Conclusão', ordemdeServico.data_de_conclusao)
    ordemdeServico.data_criacao = data.get('Data da Criação', ordemdeServico.data_criacao)
    ordemdeServico.prioridade = data.get('Prioridade', ordemdeServico.prioridade)
    ordemdeServico.observacao = data.get('Observação', ordemdeServico.observacao)
    ordemdeServico.diagnostico = data.get('diagnostico', ordemdeServico.diagnostico)
    ordemdeServico.categoria = data.get('Categoria', ordemdeServico.categoria)
    ordemdeServico.problema_relatado = data.get('Problema', ordemdeServico.problema_relatado)
    ordemdeServico.valor_servico = data.get('Valor', ordemdeServico.valor_servico)
    ordemdeServico.cliente = data.get('cliente', ordemdeServico.cliente)
    ordemdeServico.equipamento = data.get('equipamento', ordemdeServico.equipamento)
    ordemdeServico.funcionario = data.get('funcionario', ordemdeServico.funcionario)
    ordemdeServico.save()
    return Response({'status': 'success', 'message': f'Ordem com ID {id_ordem} atualizado com sucesso.'})


