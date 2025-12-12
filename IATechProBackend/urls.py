from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cliente/', include('Cliente.urls')),
    path('api/funcionario/', include('funcionario.urls')),
    path('api/equipamento/', include('equipamento.urls')),
    path('api/os/', include('OrdemdeServico.urls')),
    path('', include('core.urls'))

]


'''

| Ação                  | Método | Rota                        |
| --------------------- | ------ | --------------------------- |
| Login                 | POST   | `/auth/login/`              |
| Refresh               | POST   | `/auth/refresh/`            |
| Me                    | GET    | `/auth/me/`                 |
| Criar Funcionário     | POST   | `/api/funcionario/create/`      |
| Listar Funcionários   | GET    | `/api/funcionario/list/`        |
| Detalhar Funcionário  | GET    | `/api/funcionario/<id>/`        |
| Atualizar Funcionário | PUT    | `/api/funcionario/<id>/update/` |
| Desativar Funcionário | DELETE | `/api/funcionario/<id>/delete/` |
| Criar Cliente         | POST   | `/api/cliente/create/`          |
| Listar Clientes       | GET    | `/api/cliente/`                 |
| Detalhar Cliente      | GET    | `/api/cliente/<id>/`            |
| Atualizar Cliente     | PUT    | `/api/cliente/<id>/update/`     |
| Desativar Cliente     | DELETE | `/api/cliente/<id>/delete/`     |


Login
{
  "username": "cpf_ou_cnpj",
  "password": "senha"
}

Funcionario
{
  "username": "joao.func",
  "password": "123456",
  "email": "joao@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "cpf_cnpj": "12345678900",
  "telefone": "11999990000",
  "logradouro": "Rua A",
  "cep": "12345678",
  "cidade": "São Paulo",
  "estado": "SP",
  "especialidade": "TI",
  "cargo": "Analista",
  "salario": 5000.00
}

Cliente
{
  "username": "cliente01",
  "password": "123456",
  "email": "cliente@example.com",
  "first_name": "Carlos",
  "last_name": "Ferreira",
  "cpf_cnpj": "99911122233",
  "telefone": "11988887777",
  "logradouro": "Rua XPTO",
  "cep": "11000000",
  "cidade": "Santos",
  "estado": "SP",
  "empresa": "TechPro",
  "setor": "Compras"
}


'''