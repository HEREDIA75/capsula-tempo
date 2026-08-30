from rest_framework import permissions, viewsets
from .models import Capsula
from .serializers import CapsulaSerializer
import exifread


class CapsulaViewSet(viewsets.ModelViewSet):
    serializer_class = CapsulaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas as cápsulas pertencentes ao usuário autenticado
        return Capsula.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Salva a cápsula definindo automaticamente o usuário logado
        serializer.save(usuario=self.request.user)


def get_coordinates_from_exif(image_file):
    """Extrai lat/lng em graus decimais a partir dos metadados EXIF de uma imagem."""
    try:
        image_file.seek(0)
        tags = exifread.process_file(image_file)

        def convert_to_degrees(value):
            d = float(value.values[0].num) / float(value.values[0].den)
            m = float(value.values[1].num) / float(value.values[1].den)
            s = float(value.values[2].num) / float(value.values[2].den)
            return d + (m / 60.0) + (s / 3600.0)

        lat_tag = tags.get("GPS GPSLatitude")
        lat_ref = tags.get("GPS GPSLatitudeRef")
        lon_tag = tags.get("GPS GPSLongitude")
        lon_ref = tags.get("GPS GPSLongitudeRef")

        if lat_tag and lat_ref and lon_tag and lon_ref:
            lat = convert_to_degrees(lat_tag)
            if lat_ref.values[0] != "N":
                lat = -lat

            lon = convert_to_degrees(lon_tag)
            if lon_ref.values[0] != "E":
                lon = -lon

            return round(lat, 6), round(lon, 6)
    except Exception as e:
        print(f"Erro ao extrair EXIF: {e}")

    return None, None
