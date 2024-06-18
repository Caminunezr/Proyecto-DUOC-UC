from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import CafeViewSet, UserViewSet, MesaViewSet, CustomUserViewSet


router = DefaultRouter()
router.register(r'Cafeviewset', CafeViewSet)
router.register(r'Userviewset', UserViewSet)
router.register(r'Mesaviewset', MesaViewSet)
router.register(r'CustomUserViewSet', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]