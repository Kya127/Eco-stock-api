from rest_framework import viewsets
from .models import Warehouse, Product
from .serializers import WarehouseSerializer, ProductSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    # On dit à Django où aller chercher les données dans la BDD
    queryset = Warehouse.objects.all()
    # On lui donne le traducteur à utiliser
    serializer_class = WarehouseSerializer


class ProductViewSet(viewsets.ModelViewSet):
    # On dit à Django où aller chercher les données dans la BDD
    queryset = Product.objects.all()
    # On lui donne le traducteur à utiliser
    serializer_class = ProductSerializer