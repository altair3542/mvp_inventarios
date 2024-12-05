from django.urls import path
from .views import (
    admin_login_view,
    CategoriaListCreateView,
    CategoriaDetailView,
    ProductoListCreateView,
    ProductoDetailView,
    VentaListCreateView,
    VentaDetailView,
    ProductoBulkCreateView,
    VentaBulkCreateView,
    signup_superuser
)

# Documentación de rutas
urlpatterns = [
    # Autenticación
    path('login/', admin_login_view, name='admin_login'),  # Vista para login de superusuarios
    path('signup/', signup_superuser, name='signup-superuser'), #vista para regiastrar superusuarios

    # Endpoints de Categorías
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria_list_create'),  # Listar y crear
    path('categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria_detail'),  # Detalle, actualizar, eliminar

    # Endpoints de Productos
    path('productos/', ProductoListCreateView.as_view(), name='producto_list_create'),  # Listar y crear
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),  # Detalle, actualizar, eliminar
    path('productos/bulk-create/', ProductoBulkCreateView.as_view(), name='producto_bulk_create'),  # Crear en lote

    # Endpoints de Ventas
    path('ventas/', VentaListCreateView.as_view(), name='venta_list_create'),  # Listar y crear
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta_detail'),  # Detalle, actualizar, eliminar
    path('ventas/bulk-create/', VentaBulkCreateView.as_view(), name='venta_bulk_create'),  # Crear en lote
]
