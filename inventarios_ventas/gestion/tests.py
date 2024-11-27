from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Categoria, Producto, Venta

class CategoriaModelTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")

    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), "Electrónica")


class ProductoModelTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto = Producto.objects.create(
            nombre="Laptop",
            categoria=self.categoria,
            cantidad=10,
            precio=1500.00,
        )

    def test_producto_reducir_inventario(self):
        self.producto.reducir_inventario(5)
        self.assertEqual(self.producto.cantidad, 5)

    def test_producto_reducir_inventario_insuficiente(self):
        with self.assertRaises(Exception) as context:
            self.producto.reducir_inventario(15)
        self.assertTrue("No hay suficiente inventario" in str(context.exception))


class VentaModelTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto = Producto.objects.create(
            nombre="Laptop",
            categoria=self.categoria,
            cantidad=10,
            precio=1500.00,
        )

    def test_venta_crea_y_reduce_inventario(self):
        venta = Venta.objects.create(producto=self.producto, cantidad=5)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.cantidad, 5)
        self.assertEqual(str(venta), f"Venta de 5 Laptop el {venta.fecha}")


class ProductoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto_data = {
            "nombre": "Laptop",
            "categoria_id": self.categoria.id,
            "cantidad": 10,
            "precio": 1500.00,
        }

    def test_crear_producto(self):
        response = self.client.post("/api/productos/", self.producto_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nombre"], "Laptop")

    def test_crear_producto_precio_negativo(self):
        self.producto_data["precio"] = -1000.00
        response = self.client.post("/api/productos/", self.producto_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_productos(self):
        Producto.objects.create(**self.producto_data)
        response = self.client.get("/api/productos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_venta_sin_inventario(self):
        producto = Producto.objects.create(**self.producto_data)
        venta_data = {"producto_id": producto.id, "cantidad": 20}
        response = self.client.post("/api/ventas/", venta_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
