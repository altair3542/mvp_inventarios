from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, VentaViewSet
from django.urls import path
from .views import login_view

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)
router.register('ventas', VentaViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('login/', login_view),
] + router.urls
