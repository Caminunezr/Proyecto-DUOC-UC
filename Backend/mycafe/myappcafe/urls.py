from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoViewSet, IngredienteViewSet, RecetaViewSet, 
    VentaViewSet, UserViewSet, MesaViewSet, ReservaViewSet, 
    BoletaViewSet, UserRegisterView, UserLoginView, user_info, save_message, ContactMessageViewSet
)

# Configuración del router
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'recetas', RecetaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'users', UserViewSet)
router.register(r'mesas', MesaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'boletas', BoletaViewSet)
router.register(r'mensajes', ContactMessageViewSet)

# Configuración de las URLs
urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user-info/', user_info, name='user_info'),
    path('contact-message/', save_message, name='contact_message'),
]