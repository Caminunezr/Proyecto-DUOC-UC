from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import CafeViewSet, UserViewSet


router = DefaultRouter()
router.register(r'Cafeviewset', CafeViewSet)
router.register(r'Userviewset', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]