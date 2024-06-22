from rest_framework import serializers
from .models import Producto, Ingrediente, Receta, Venta
from django.contrib.auth.models import User


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ['id', 'nombre', 'cantidad_en_stock', 'unidad_medida']
        

class RecetaSerializer(serializers.ModelSerializer):
    ingrediente_detalle = IngredienteSerializer(source='ingrediente', read_only=True)

    class Meta:
        model = Receta
        fields = ['id', 'producto', 'ingrediente', 'ingrediente_detalle', 'cantidad_necesaria']
        
class ProductoSerializer(serializers.ModelSerializer):
    recetas = RecetaSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'disponible', 'requiere_receta', 'cantidad_en_stock', 'recetas']

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.requiere_receta = validated_data.get('requiere_receta', instance.requiere_receta)
        instance.cantidad_en_stock = validated_data.get('cantidad_en_stock', instance.cantidad_en_stock)
        instance.save()
        instance.actualizar_disponibilidad()
        return instance

class VentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), source='producto', write_only=True
    )
    total_venta = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = ['id', 'producto', 'producto_id', 'cantidad', 'fecha_hora', 'total_venta']

    def get_total_venta(self, obj):
        return obj.total_venta

    def create(self, validated_data):
        producto = validated_data['producto']
        cantidad = validated_data['cantidad']
        producto.vender_producto(cantidad)  # Descuenta el stock de los ingredientes
        venta = Venta.objects.create(**validated_data)
        return venta
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
