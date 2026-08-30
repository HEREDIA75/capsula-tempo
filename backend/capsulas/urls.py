from django.urls import path
from . import views

# O app_name ajuda a organizar os URLs (namespaces)
app_name = "capsula"

urlpatterns = [
    # Exemplo: página inicial da cápsula (http://127.0.0.1:8000/capsula/)
    path("", views.index, name="index"),
    # Exemplo: detalhe de uma cápsula específica pelo ID (http://127.0.0.1:8000/capsula/1/)
    path("<int:pk>/", views.detalhe, name="detalhe"),
    # Exemplo: criar uma nova cápsula (http://127.0.0.1:8000/capsula/criar/)
    path("criar/", views.criar, name="criar"),
]
