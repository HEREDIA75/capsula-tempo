from django.db import models


class Capsula(models.Model):
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_revelacao = models.DateTimeField()

    def __str__(self):
        return self.titulo
