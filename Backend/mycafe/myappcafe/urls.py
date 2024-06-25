from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, IngredienteViewSet, RecetaViewSet, VentaViewSet, ReservaViewSet, UserViewSet, MesaViewSet, UserRegisterView, UserLoginView, BoletaViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'recetas', RecetaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'usuarios', UserViewSet)
router.register(r'mesas', MesaViewSet)
router.register(r'boletas', BoletaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]
