from rest_framework import viewsets
from .models import Producto, Ingrediente, Receta, Venta, Mesa, Reserva,CustomUser
from .serializers import ProductoSerializer, IngredienteSerializer, RecetaSerializer, VentaSerializer, UserSerializer, MesaSerializer, ReservaSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
