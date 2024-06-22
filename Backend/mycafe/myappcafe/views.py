from rest_framework import viewsets
from .models import Producto, Ingrediente, Receta, Venta
from .serializers import ProductoSerializer, IngredienteSerializer, RecetaSerializer, VentaSerializer, UserSerializer
from django.contrib.auth.models import User

class ProductoViewSet(viewsets.ModelViewSet):
    """
    Un viewset para ver, editar y eliminar productos.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def perform_create(self, serializer):
        serializer.save()

class IngredienteViewSet(viewsets.ModelViewSet):
    """
    Un viewset para ver, editar y eliminar ingredientes.
    """
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer

class RecetaViewSet(viewsets.ModelViewSet):
    """
    Un viewset para ver, editar y eliminar recetas.
    """
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Un viewset para ver, editar y eliminar usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
