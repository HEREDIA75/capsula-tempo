from rest_framework import serializers
from .models import Capsula


class CapsulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capsula
        fields = "__all__"
