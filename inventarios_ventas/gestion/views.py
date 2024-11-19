from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import Producto, Venta
from .forms import VentaForm
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Categoria, Producto, Venta
from .serializers import CategoriaSerializer, ProductoSerializer, VentaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


# Vista para listar los productos
class ListaProductosView(ListView):
    model = Producto
    template_name = 'gestion/lista_productos.html'
    context_object_name = 'productos'

# Vista para registrar una venta
@method_decorator(csrf_protect, name='dispatch')
class RegistrarVentaView(FormView):
    template_name = 'gestion/registrar_venta.html'
    form_class = VentaForm

    def form_valid(self, form):
        producto_id = self.kwargs['producto_id']
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = form.cleaned_data['cantidad']
        if producto.cantidad >= cantidad:
            Venta.objects.create(producto=producto, cantidad=cantidad)
            producto.cantidad -= cantidad
            producto.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lista_productos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['producto'] = get_object_or_404(Producto, id=self.kwargs['producto_id'])
        return context


#vistas para las apis
# Vistas para Categorías
class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vistas para Productos
class ProductoListCreateView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vistas para Ventas
class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

class VentaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductoBulkCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not isinstance(request.data, list):
            return Response({"error": "Se espera una lista de productos"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductoSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VentaBulkCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not isinstance(request.data, list):
            return Response({"error": "Se espera una lista de ventas"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VentaSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

