from rest_framework import permissions, viewsets
from .models import Capsula
from .serializers import CapsulaSerializer


class CapsulaViewSet(viewsets.ModelViewSet):
    serializer_class = CapsulaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as cápsulas pertencentes ao usuário autenticado
        return Capsula.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Salva a cápsula definindo automaticamente o usuário logado
        serializer.save(usuario=self.request.user)
