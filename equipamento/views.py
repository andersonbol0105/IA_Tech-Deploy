from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth.models import User
from django.utils.dateformat import format
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response 

# Importe seu modelo
from .models import Equipamento

def _serialize_Equipamento(equipamento):
    return {
         'id': equipamento.id,
        'modelo_marca': equipamento.modelo_marca,
        'patrimonio': equipamento.patrimonio,
        'num_serie': equipamento.num_serie,
    }

@api_view(['GET'])
def py_obter_equipamento(request, id_equipamento=None):
    if id_equipamento:
        try:
            equipamento = Equipamento.objects.get(pk=id_equipamento)
            equipamento_data = _serialize_Equipamento(equipamento)
            return Response({'Equipamento': equipamento_data})
        except Equipamento.DoesNotExist:
            return Response({'error': 'Equipamento não encontrado.'}, status=404)
    else:
        equipamento = Equipamento.objects.all()
        equipamento_data = [_serialize_Equipamento(equipamento) for equipamento in equipamento]
        return Response({'equipamento':equipamento_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def py_cria_equipamento(request):
    data = request.data
    equipamento = Equipamento.objects.create(
        id_equipamento=data.get('id_equipamento'),
        modelo_marca=data.get('modelo_marca'),
        patrimonio=data.get('patrimonio'),
        num_serie=data.get('num_serie'),
    )
    return Response({'status': 'success', 'id_equipameto': id.equipamento}, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def py_deleta_equipamento(request, id_equipamento):
    """
    Função para deletar um equipamento especifico.
    """
    equipamento = get_object_or_404(Equipamento, pk=id_equipamento)
    equipamento.delete()
    return Response({'status': 'success', 'message': f'Equipamento com ID {id_equipamento} deletado com sucesso.' })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def py_edita_equipamento(request, id_equipamento):
    equipamento = get_object_or_404(Equipamento, pk=id_equipamento)
    data = request.data
    # Atualiza apenas os campos presentes no JSON
    equipamento.id_equipamento = data.get('id_equipamento', equipamento.id_equipamento)
    equipamento.modelo_marca = data.get('modelo_marca', equipamento.modelo_marca)
    equipamento.patrimonio = data.get('patrimonio', equipamento.patrimonio)
    equipamento.num_serie = data.get('num_serie', equipamento.num_serie)
    equipamento.save()
    return Response({'status': 'success', 'message': f'Equipamento com ID {id_equipamento} atualizado com sucesso.'})