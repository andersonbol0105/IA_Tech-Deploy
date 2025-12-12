from django.contrib import admin
from .models import Equipamento

# Register your models here.
class EquipamentoAdmin(admin.ModelAdmin):
    list_display=('modelo_marca','patrimonio','num_serie')
    search_fields=('modelo_marca','patrimonio','num_serie')
    list_filter=('modelo_marca','patrimonio','num_serie')

admin.site.register(Equipamento, EquipamentoAdmin)