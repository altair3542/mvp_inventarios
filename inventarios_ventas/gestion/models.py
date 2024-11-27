from django.db import models

# Create your models here.
from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)  # Índice para mejorar búsquedas

    def __str__(self):
        return str(self.nombre)

class Producto(models.Model):
    nombre = models.CharField(max_length=100, db_index=True)  # Índice para mejorar búsquedas
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)  # Asegura valores positivos
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} (Categoría: {self.categoria.nombre})"

    def reducir_inventario(self, cantidad):
        """
        Reduce el inventario si hay suficiente stock disponible.
        """
        if cantidad > self.cantidad:
            raise ValidationError("No hay suficiente inventario disponible.")
        self.cantidad -= cantidad
        self.save()

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venta de {self.cantidad} unidad(es) de {self.producto.nombre} el {self.fecha}"

    def save(self, *args, **kwargs):
        """
        Sobreescribe el método save para validar y actualizar inventario de forma atómica.
        """
        with transaction.atomic():
            self.producto.reducir_inventario(self.cantidad)
            super().save(*args, **kwargs)
