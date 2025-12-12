from django.contrib import admin
from django import forms
from .models import Cliente
from core.models import User


class ClienteAdminForm(forms.ModelForm):
    # Campos do User
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
        model = Cliente
        fields = ["empresa", "setor"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Se estiver editando um Cliente existente, carregar dados do User
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

            # Senha não pode ser exibida — só muda se escrever uma nova
            self.fields["password"].required = False

    def save(self, commit=True):
        """Cria ou atualiza o User associado ao Cliente."""

        if self.instance and self.instance.pk:
            # Atualizando usuário existente
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
            user.role = "Cliente"

            if self.cleaned_data.get("password"):
                user.set_password(self.cleaned_data["password"])

            user.save()

        else:
            # Criar novo usuário
            password = self.cleaned_data["password"] or User.objects.make_random_password()

            user = User.objects.create_user(
                username=self.cleaned_data["username"],
                email=self.cleaned_data.get("email"),
                password=password,
                role="Cliente",
                first_name=self.cleaned_data.get("first_name"),
                last_name=self.cleaned_data.get("last_name"),
                cpf_cnpj=self.cleaned_data["cpf_cnpj"],
                telefone=self.cleaned_data.get("telefone", ""),
                logradouro=self.cleaned_data.get("logradouro", ""),
                cep=self.cleaned_data.get("cep", ""),
                cidade=self.cleaned_data.get("cidade", ""),
                estado=self.cleaned_data.get("estado", ""),
            )

        cliente = super().save(commit=False)
        cliente.user = user

        if commit:
            cliente.save()

        return cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm

    list_display = ("id", "empresa", "setor", "user")
    list_display_links = ("id", "empresa")
    search_fields = ("empresa", "setor", "user__username", "user__first_name")
    list_filter = ("setor", "empresa")
    ordering = ("empresa",)
