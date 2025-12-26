from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Equipamento

# Função auxiliar para serializar os dados
def _serialize_equipamento(equipamento):
    return {
        'id': equipamento.id,
        'modelo_marca': equipamento.modelo_marca,
        'patrimonio': equipamento.patrimonio,
        'num_serie': equipamento.num_serie,
        'ativo': equipamento.ativo,
    }

# ===================== LISTAR / OBTER =====================
@api_view(['GET'])
def py_obter_equipamento(request, id_equipamento=None):
    if id_equipamento:
        equipamento = get_object_or_404(Equipamento, pk=id_equipamento)
        equipamento_data = _serialize_equipamento(equipamento)
        return Response({'equipamento': equipamento_data})
    else:
        equipamentos = Equipamento.objects.all()
        equipamento_data = [_serialize_equipamento(e) for e in equipamentos]
        return Response({'equipamento': equipamento_data})

# ===================== CRIAR =====================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def py_cria_equipamento(request):
    data = request.data

    ativo_value = data.get('ativo', True)
    # garante que qualquer valor seja convertido para boolean
    ativo_bool = str(ativo_value).lower() in ['true', '1', 'yes', 't']

    equipamento = Equipamento.objects.create(
        modelo_marca=data.get('modelo_marca'),
        patrimonio=data.get('patrimonio'),
        num_serie=data.get('num_serie'),
        ativo=ativo_bool
    )
    return Response({'status': 'success', 'id': equipamento.id}, status=201)


# ===================== DELETAR =====================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def py_deleta_equipamento(request, id_equipamento):
    equipamento = get_object_or_404(Equipamento, pk=id_equipamento)
    equipamento.delete()
    return Response({'status': 'success', 'message': f'Equipamento com ID {id_equipamento} deletado com sucesso.'})

# ===================== EDITAR =====================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def py_edita_equipamento(request, id_equipamento):
    equipamento = get_object_or_404(Equipamento, pk=id_equipamento)
    data = request.data

    equipamento.modelo_marca = data.get('modelo_marca', equipamento.modelo_marca)
    equipamento.patrimonio = data.get('patrimonio', equipamento.patrimonio)
    equipamento.num_serie = data.get('num_serie', equipamento.num_serie)
    equipamento.ativo = data.get('ativo', equipamento.ativo)

    equipamento.save()
    return Response({'status': 'success', 'message': f'Equipamento com ID {id_equipamento} atualizado com sucesso.'})
