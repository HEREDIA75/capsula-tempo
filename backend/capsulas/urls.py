from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from capsulas.views import CapsulaViewSet

router = DefaultRouter()
router.register(r"capsulas", CapsulaViewSet, basename="capsula")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
