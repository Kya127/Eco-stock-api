from rest_framework import serializers
from .models import Warehouse, Product

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'  # Signifie qu'on veut traduire tous les champs (id, nom, localisation, capacite)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 