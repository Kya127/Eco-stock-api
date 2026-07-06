from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, ProductViewSet

# Le routeur est un outil automatique qui crée les bonnes adresses URL par exemple POST GET PUT DELETE
router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]