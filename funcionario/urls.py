from django.urls import path
from .views import (
    FuncionarioCreateView,
    FuncionarioListView,
    FuncionarioDetailView,
    FuncionarioUpdateView,
    FuncionarioDeleteView
)

urlpatterns = [
    path("create/", FuncionarioCreateView.as_view(), name="funcionario-create"),
    path("list/", FuncionarioListView.as_view(), name="funcionario-list"),
    path("<int:pk>/", FuncionarioDetailView.as_view(), name="funcionario-detail"),
    path("<int:pk>/update/", FuncionarioUpdateView.as_view(), name="funcionario-update"),
    path("<int:pk>/delete/", FuncionarioDeleteView.as_view(), name="funcionario-delete"),
]
