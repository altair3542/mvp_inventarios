from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import Categoria, Producto, Venta
from .serializers import CategoriaSerializer, ProductoSerializer, VentaSerializer
from .forms import VentaForm

# Vista de Login para Superusuarios

@api_view(["POST"]) #solo metodos post
@permission_classes([AllowAny])

def admin_login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user and user.is_superuser:
        login(request, user)
        return Response({"message": "SuperUser login successful"}, status=200)

    return Response({"error": "Credenciales inválidas o usuario no autorizado"}, status=403)

@api_view(["POST"])
@permission_classes([AllowAny])  # Permite acceso sin autenticación
def signup_superuser(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    # Validar datos enviados
    if not username or not password or not email:
        return Response({"error": "Se requieren 'username', 'password' y 'email'"}, status=400)

    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        return Response({"error": "El usuario ya existe"}, status=400)

    # Crear el superusuario
    try:
        superuser = User.objects.create_superuser(username=username, password=password, email=email)
        return Response({"message": f"Superusuario '{superuser.username}' creado exitosamente"}, status=201)
    except Exception as e:
        return Response({"error": f"Error al crear el superusuario: {str(e)}"}, status=500)


# Vista para Registrar Venta
@method_decorator(csrf_protect, name="dispatch")
class RegistrarVentaView(FormView):
    template_name = "gestion/registrar_venta.html"
    form_class = VentaForm

    def form_valid(self, form):
        producto_id = self.kwargs["producto_id"]
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = form.cleaned_data["cantidad"]

        with transaction.atomic():
            producto.reducir_inventario(cantidad)  # Usa el método del modelo mejorado
            Venta.objects.create(producto=producto, cantidad=cantidad)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("lista_productos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["producto"] = get_object_or_404(Producto, id=self.kwargs["producto_id"])
        return context


# Clase Base para Vistas Genéricas
class BaseModelViewSet:
    permission_classes = [permissions.IsAuthenticated]


# Vistas para Categorías
class CategoriaListCreateView(BaseModelViewSet, generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class CategoriaDetailView(BaseModelViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


# Vistas para Productos
class ProductoListCreateView(BaseModelViewSet, generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class ProductoDetailView(BaseModelViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# Vistas para Ventas
class VentaListCreateView(BaseModelViewSet, generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer


class VentaDetailView(BaseModelViewSet, generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer


# Vista Reutilizable para Creación Masiva
class BulkCreateAPIView(BaseModelViewSet, APIView):
    model = None
    serializer_class = None

    def post(self, request):
        if not isinstance(request.data, list):
            return Response(
                {"error": "Se espera una lista de objetos"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista Específica para Productos y Ventas
class ProductoBulkCreateView(BulkCreateAPIView):
    model = Producto
    serializer_class = ProductoSerializer


class VentaBulkCreateView(BulkCreateAPIView):
    model = Venta
    serializer_class = VentaSerializer
