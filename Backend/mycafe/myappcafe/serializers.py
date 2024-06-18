from rest_framework import serializers
from .models import Cafe, Mesa, CustomUser 
from django.contrib.auth.models import User

class CafeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Cafe
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = '__all__'

class MesaSerializer(serializers.ModelSerializer):
    class meta:
        model = Mesa
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class meta:
        model = CustomUser
        fields = '__all__'
