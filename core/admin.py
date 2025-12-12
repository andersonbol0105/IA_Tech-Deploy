from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Campos que serão exibidos na listagem
    list_display = ('username', 'email', 'role', 'cpf_cnpj', 'telefone', 'cidade', 'estado', 'is_staff')

    # Campos que podem ser usados para busca
    search_fields = ('username', 'email', 'cpf_cnpj', 'telefone', 'role')

    # Organização dos campos nos formulários
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Informações pessoais', {
            'fields': (
                'first_name', 'last_name', 'email',
                'cpf_cnpj', 'telefone', 'logradouro',
                'cep', 'cidade', 'estado'
            )
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos exibidos no formulário de criação de usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 'role',
                'cpf_cnpj', 'telefone', 'logradouro',
                'cep', 'cidade', 'estado'
            ),
        }),
    )
