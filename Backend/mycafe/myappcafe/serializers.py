from rest_framework import serializers
from .models import Cafe  
from django.contrib.auth.models import User

class CafeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Cafe
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = '__all__'
