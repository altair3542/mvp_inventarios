from django.db import models

# Create your models here.
from django.db import models

class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos.
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Modelo que representa un producto dentro de una categoría.
    """
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="productos"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    def reducir_stock(self, cantidad):
        """
        Reduce el stock del producto en la cantidad especificada.
        """
        if cantidad > self.stock:
            raise ValueError("No hay suficiente stock disponible.")
        self.stock -= cantidad
        self.save()


class Venta(models.Model):
    """
    Modelo que representa una venta de un producto.
    """
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="ventas"
    )
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        """
        Calcula el monto total de la venta.
        """
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"Venta de {self.cantidad} {self.producto.nombre}"

    def save(self, *args, **kwargs):
        """
        Reduce el stock del producto al registrar la venta.
        """
        self.producto.reducir_stock(self.cantidad)
        super().save(*args, **kwargs)
