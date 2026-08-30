from rest_framework import viewsets
from .models import Capsula
from .serializers import CapsulaSerializer


class CapsulaViewSet(viewsets.ModelViewSet):
    queryset = Capsula.objects.all()
    serializer_class = CapsulaSerializer
