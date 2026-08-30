from datetime import timedelta
from capsulas.models import Capsula
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient


class CapsulaAPITestCase(TestCase):

    def setUp(self):
        # Criar usuários de teste
        self.user1 = User.objects.create_user(
            username="usuario1", password="senha123password"
        )
        self.user2 = User.objects.create_user(
            username="usuario2", password="senha123password"
        )

        # Instanciar cliente API REST
        self.client = APIClient()

        # Obter token JWT para o usuario1
        response = self.client.post(
            "/api/token/",
            {"username": "usuario1", "password": "senha123password"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data["access"]

        # Definir datas para os testes
        self.data_futura = timezone.now() + timedelta(days=30)
        self.data_passada = timezone.now() - timedelta(days=1)

        # Criar cápsulas associadas
        self.capsula1 = Capsula.objects.create(
            usuario=self.user1,
            titulo="Cápsula do Usuario 1",
            conteudo="Conteúdo Secreto 1",
            latitude=-23.550520,
            longitude=-46.633308,
            data_revelacao=self.data_futura,
        )

        self.capsula2 = Capsula.objects.create(
            usuario=self.user2,
            titulo="Cápsula do Usuario 2",
            conteudo="Conteúdo Secreto 2",
            data_revelacao=self.data_futura,
        )

    def test_autenticacao_obrigatoria(self):
        """Garante que requisições sem Bearer token retornam HTTP 401."""
        response = self.client.get("/api/capsulas/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obter_token_jwt(self):
        """Testa a geração de token JWT no endpoint /api/token/."""
        response = self.client.post(
            "/api/token/",
            {"username": "usuario1", "password": "senha123password"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_listar_apenas_capsulas_do_usuario_autenticado(self):
        """Garante o isolamento de cápsulas entre contas diferentes."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get("/api/capsulas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["titulo"], "Cápsula do Usuario 1")

    def test_criar_capsula_com_coordenadas(self):
        """Testa criação de cápsula fornecendo latitude e longitude."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        data = {
            "titulo": "Viagem a Sintra",
            "conteudo": "Lembrança do Palácio da Pena",
            "latitude": 38.787833,
            "longitude": -9.390500,
            "data_revelacao": self.data_futura.isoformat(),
        }
        response = self.client.post("/api/capsulas/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["usuario"], "usuario1")
        self.assertEqual(response.data["latitude"], 38.787833)

    def test_criar_capsula_sem_coordenadas_opcionais(self):
        """Testa criação de cápsula omitindo as coordenadas opcionais."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        data = {
            "titulo": "Cápsula Sem Localização",
            "conteudo": "Apenas texto e data",
            "data_revelacao": self.data_futura.isoformat(),
        }
        response = self.client.post("/api/capsulas/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["latitude"])
        self.assertIsNone(response.data["longitude"])

    def test_upload_imagem_capsula(self):
        """Testa envio de imagem via formulário multipart."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00"
            b"\x01\x00\x80\x00\x00\xff\xff\xff"
            b"\x00\x00\x00\x21\xf9\x04\x01\x00"
            b"\x00\x00\x00\x2c\x00\x00\x00\x00"
            b"\x01\x00\x01\x00\x00\x02\x02\x44"
            b"\x01\x00\x3b"
        )
        foto = SimpleUploadedFile("teste.gif", small_gif, content_type="image/gif")

        data = {
            "titulo": "Foto da Praia",
            "conteudo": "Dia de sol",
            "data_revelacao": self.data_futura.isoformat(),
            "imagem": foto,
        }
        response = self.client.post("/api/capsulas/", data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["imagem"])
