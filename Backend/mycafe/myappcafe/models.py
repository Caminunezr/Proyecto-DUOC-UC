from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser

# Opciones para las unidades de medidas respaldo
UNIDAD_MEDIDA_OPCIONES = (
    ('G', 'gramos'),
    ('Kg', 'kilogramos'),
    ('L', 'litros'),
    ('Ml', 'mililitros'),
)

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.email


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    requiere_receta = models.BooleanField(default=False)
    cantidad_en_stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def actualizar_disponibilidad(self):
        if self.requiere_receta:
            self.disponible = all(receta.ingrediente.cantidad_en_stock >= receta.cantidad_necesaria for receta in self.recetas.all())
        else:
            self.disponible = self.cantidad_en_stock > 0
        self.save()

    def vender_producto(self, cantidad):
        cantidad = int(cantidad)
        if not self.disponible:
            raise ValueError("Este producto no está disponible para la venta.")

        if self.requiere_receta:
            for receta in self.recetas.all():
                if receta.ingrediente.cantidad_en_stock < receta.cantidad_necesaria * Decimal(cantidad):
                    raise ValueError(f"Stock insuficiente para el ingrediente: {receta.ingrediente.nombre}")
        self.cantidad_en_stock -= cantidad
        self.save()


class Receta(models.Model):
    producto = models.ForeignKey(Producto, related_name='recetas', on_delete=models.CASCADE)
    ingrediente = models.ForeignKey('Ingrediente', related_name='ingrediente_recetas', on_delete=models.CASCADE)
    cantidad_necesaria = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad_necesaria} de {self.ingrediente.nombre} para {self.producto.nombre}"


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_hora = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} vendido/s el {self.fecha_hora}"

    @property
    def precio_venta(self):
        return self.producto.precio * Decimal(self.cantidad)


class Mesa(models.Model):
    CAPACIDAD_CHOICES = [
        (1, '1 persona'),
        (2, '2 personas'),
        (3, '3 personas'),
        (4, '4 personas'),
        (5, '5 o más personas'),
    ]
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField(choices=CAPACIDAD_CHOICES)

    def __str__(self):
        return f"Mesa {self.numero} - {self.get_capacidad_display()}"


class Reserva(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100, default="Unknown")
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()

    def __str__(self):
        return f"Reserva para {self.nombre_cliente} en {self.mesa} desde {self.fecha_hora_inicio} hasta {self.fecha_hora_fin}"

    def clean(self):
        """Validate that the reservation does not overlap with existing reservations."""
        super().clean()
        if self.fecha_hora_inicio >= self.fecha_hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        overlapping_reservations = Reserva.objects.filter(
            mesa=self.mesa,
            fecha_hora_fin__gt=self.fecha_hora_inicio,
            fecha_hora_inicio__lt=self.fecha_hora_fin,
        ).exclude(pk=self.pk)
        if overlapping_reservations.exists():
            raise ValidationError("Ya existe una reserva para esta mesa en el periodo seleccionado.")

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_en_stock = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nombre