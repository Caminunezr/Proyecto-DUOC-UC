from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Cafe, Mesa, CustomUser
from .serializers import CafeSerializer, UserSerializer, MesaSerializer, CustomUserSerializer

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer