from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Categoria, Producto, Venta
from .serializers import CategoriaSerializer, ProductoSerializer, VentaSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({"message": "Login exitoso"})
    return JsonResponse({"error": "Credenciales inválidas"}, status=403)

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("Usuario autenticado:", request.user)
        print("Session Key:", request.session.session_key)
        return super().get(request, *args, **kwargs)


@api_view(["POST"])
@permission_classes([AllowAny])  # Permitir el acceso sin autenticación
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    # Validar que los campos no estén vacíos
    if not username or not password or not email:
        return Response(
            {"error": "Todos los campos son obligatorios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validar si el nombre de usuario ya existe
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "El nombre de usuario ya está en uso."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Crear el usuario
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "Usuario registrado con éxito."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {"error": f"Error al registrar el usuario: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

class VentaViewSet(ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]
