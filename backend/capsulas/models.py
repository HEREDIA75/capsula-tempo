from django.contrib.auth.models import User
from django.db import models


class Capsula(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="capsulas")
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    imagem = models.ImageField(upload_to="capsulas/", null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_revelacao = models.DateTimeField()

    def __str__(self):
        return f"{self.titulo} ({self.usuario.username})"
