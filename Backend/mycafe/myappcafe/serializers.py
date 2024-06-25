from rest_framework import serializers
from .models import Producto, Ingrediente, Receta, Venta, Mesa, Reserva, UserProfile, CustomUser, Boleta

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'birth_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'birth_date', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date'],
            password=validated_data['password']
        )
        return user

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['numero', 'capacidad']

class ReservaSerializer(serializers.ModelSerializer):
    mesa_detalle = MesaSerializer(source='mesa', read_only=True)

    class Meta:
        model = Reserva
        fields = ['id', 'mesa', 'mesa_detalle', 'usuario', 'nombre_cliente', 'fecha_hora_inicio', 'fecha_hora_fin']

    def validate(self, data):
        """Custom validation for overlapping reservations."""
        mesa = data['mesa']
        fecha_hora_inicio = data['fecha_hora_inicio']
        fecha_hora_fin = data['fecha_hora_fin']
        
        if fecha_hora_inicio >= fecha_hora_fin:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        
        overlapping_reservations = Reserva.objects.filter(
            mesa=mesa,
            fecha_hora_fin__gt=fecha_hora_inicio,
            fecha_hora_inicio__lt=fecha_hora_fin,
        )
        if self.instance:
            overlapping_reservations = overlapping_reservations.exclude(pk=self.instance.pk)

        if overlapping_reservations.exists():
            raise serializers.ValidationError("Ya existe una reserva para esta mesa en el periodo seleccionado.")

        return data

class BoletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boleta
        fields = ['id', 'usuario', 'venta', 'nombre_usuario', 'fecha_hora', 'metodo_pago']
