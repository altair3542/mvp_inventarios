from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, VentaViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import signup

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)
router.register('ventas', VentaViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("signup/", signup, name="signup"),
] + router.urls
