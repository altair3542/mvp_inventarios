from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ListaProductosView, RegistrarVentaView,
    CategoriaListCreateView, CategoriaDetailView,
    ProductoListCreateView, ProductoDetailView,
    VentaListCreateView, VentaDetailView,
    ProductoBulkCreateView, VentaBulkCreateView,
    admin_login_view
)

urlpatterns = [
    path('', ListaProductosView.as_view(), name='lista_productos'),
    path('registrar-venta/<int:producto_id>/', RegistrarVentaView.as_view(), name='registrar_venta'),
    path('categorias/', CategoriaListCreateView.as_view(), name='categoria_list_create'),
    path('categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria_detail'),
    path('productos/', ProductoListCreateView.as_view(), name='producto_list_create'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('ventas/', VentaListCreateView.as_view(), name='venta_list_create'),
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('productos/bulk-create/', ProductoBulkCreateView.as_view(), name='producto_bulk_create'),
    path('ventas/bulk-create/', VentaBulkCreateView.as_view(), name='venta_bulk_create'),
    path('admin-login/', admin_login_view, name='admin_login'), 
]
