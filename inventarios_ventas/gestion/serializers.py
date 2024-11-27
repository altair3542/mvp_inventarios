from rest_framework import serializers
from .models import Categoria, Producto, Venta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']  # Especificamos los campos a incluir

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)  # Incluye la relación como un serializer anidado
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), write_only=True
    )  # Campo para enviar el ID en operaciones de escritura

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'categoria_id', 'cantidad', 'precio']

    def validate_precio(self, value):
        """
        Valida que el precio no sea negativo.
        """
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

class VentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)  # Serializa detalles del producto
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), write_only=True
    )  # Campo para enviar el ID en operaciones de escritura

    class Meta:
        model = Venta
        fields = ['id', 'producto', 'producto_id', 'cantidad', 'fecha']

    def validate_cantidad(self, value):
        """
        Valida que la cantidad sea positiva y no exceda el inventario.
        """
        producto = self.initial_data.get('producto_id')
        if not producto:
            raise serializers.ValidationError("Debe especificarse un producto.")

        producto_obj = Producto.objects.get(id=producto)
        if value > producto_obj.cantidad:
            raise serializers.ValidationError(
                f"No hay suficiente inventario disponible. Solo quedan {producto_obj.cantidad} unidades."
            )
        return value
