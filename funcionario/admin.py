# funcionario/admin.py
from django.contrib import admin
from django import forms
from .models import Funcionario
from core.models import User


class FuncionarioAdminForm(forms.ModelForm):
    # Campos do User (editáveis)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    cpf_cnpj = forms.CharField(required=True)
    telefone = forms.CharField(required=False)
    logradouro = forms.CharField(required=False)
    cep = forms.CharField(required=False)
    cidade = forms.CharField(required=False)
    estado = forms.CharField(required=False)

    class Meta:
        model = Funcionario
        fields = ["especialidade", "cargo", "salario"]  # <-- REMOVIDO data_admissao

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Quando editando, carregar dados do usuário
        if self.instance and self.instance.pk:
            user = self.instance.user

            self.fields["username"].initial = user.username
            self.fields["email"].initial = user.email
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["cpf_cnpj"].initial = user.cpf_cnpj
            self.fields["telefone"].initial = user.telefone
            self.fields["logradouro"].initial = user.logradouro
            self.fields["cep"].initial = user.cep
            self.fields["cidade"].initial = user.cidade
            self.fields["estado"].initial = user.estado

            self.fields["password"].required = False

    def save(self, commit=True):
        """Cria ou atualiza o User vinculado ao Funcionario."""

        if self.instance and self.instance.pk:
            # Atualizando
            user = self.instance.user
            user.username = self.cleaned_data["username"]
            user.email = self.cleaned_data.get("email")
            user.first_name = self.cleaned_data.get("first_name")
            user.last_name = self.cleaned_data.get("last_name")
            user.cpf_cnpj = self.cleaned_data["cpf_cnpj"]
            user.telefone = self.cleaned_data.get("telefone", "")
            user.logradouro = self.cleaned_data.get("logradouro", "")
            user.cep = self.cleaned_data.get("cep", "")
            user.cidade = self.cleaned_data.get("cidade", "")
            user.estado = self.cleaned_data.get("estado", "")
            user.is_staff = True
            user.role = "Funcionario"

            if self.cleaned_data.get("password"):
                user.set_password(self.cleaned_data["password"])

            user.save()

        else:
            # Criando novo
            password = self.cleaned_data["password"] or User.objects.make_random_password()

            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                email=self.cleaned_data.get("email"),
                password=password,
                is_staff=True,
                role="Funcionario",
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                cpf_cnpj=self.cleaned_data["cpf_cnpj"],
                telefone=self.cleaned_data.get("telefone", ""),
                logradouro=self.cleaned_data.get("logradouro", ""),
                cep=self.cleaned_data.get("cep", ""),
                cidade=self.cleaned_data.get("cidade", ""),
                estado=self.cleaned_data.get("estado", ""),
            )

        funcionario = super().save(commit=False)
        funcionario.user = user

        if commit:
            funcionario.save()

        return funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    form = FuncionarioAdminForm

    list_display = (
        "id",
        "get_nome",
        "get_email",
        "especialidade",
        "cargo",
        "salario",
        "data_admissao",
    )

    list_display_links = ("id", "get_nome")
    search_fields = ("user__first_name", "user__last_name", "user__email", "especialidade", "cargo")
    list_filter = ("especialidade", "cargo", "data_admissao")
    ordering = ("-data_admissao",)
    list_per_page = 12

    def get_nome(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_nome.short_description = "Nome"

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
