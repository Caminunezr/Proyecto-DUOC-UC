from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Cafe
from .serializers import CafeSerializer, UserSerializer

class CafeViewSet(viewsets.ModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer