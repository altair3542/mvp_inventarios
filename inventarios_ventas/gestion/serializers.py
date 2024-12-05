from rest_framework import serializers
from .models import Categoria, Producto, Venta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre']  # Incluye solo los campos necesarios

class VentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)  # Incluir el objeto completo del producto

    class Meta:
        model = Venta
        fields = ['id', 'producto', 'cantidad', 'total', 'fecha']
