from rest_framework import serializers
from .models import Capsula


class CapsulaSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source="usuario.username")

    class Meta:
        model = Capsula
        fields = "__all__"
