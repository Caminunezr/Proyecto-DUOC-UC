from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, IngredienteViewSet, RecetaViewSet, VentaViewSet, UserViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'recetas', RecetaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]