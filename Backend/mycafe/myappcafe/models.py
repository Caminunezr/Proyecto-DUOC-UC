from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

# Opciones para las unidades de medidas respaldo
UNIDAD_MEDIDA_OPCIONES = (
    ('G', 'gramos'),
    ('MG', 'miligramos'),
)

# Opciones para los métodos de pago
METODO_PAGO_OPCIONES = (
    ('EFECTIVO', 'Efectivo'),
    ('TARJETA_DEBITO', 'Tarjeta Débito'),
    ('TARJETA_CREDITO', 'Tarjeta Crédito'),
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
    descripcion = models.TextField(blank=True, null=True)  # Añadir descripción
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    requiere_receta = models.BooleanField(default=False)
    cantidad_en_stock = models.IntegerField(default=0)
    categoria = models.CharField(max_length=100, default='General')

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
                if receta.ingrediente.cantidad_en_stock < receta.cantidad_necesaria * cantidad:
                    raise ValueError(f"Stock insuficiente para el ingrediente: {receta.ingrediente.nombre}")
                receta.ingrediente.cantidad_en_stock -= receta.cantidad_necesaria * cantidad
                receta.ingrediente.save()
        else:
            if self.cantidad_en_stock < cantidad:
                raise ValueError("Stock insuficiente para este producto.")
            self.cantidad_en_stock -= cantidad
            self.save()

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_en_stock = models.DecimalField(max_digits=8, decimal_places=2)
    unidad_medida = models.CharField(max_length=2, choices=UNIDAD_MEDIDA_OPCIONES, default='G')

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    producto = models.ForeignKey(Producto, related_name='recetas', on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, related_name='ingrediente_recetas', on_delete=models.CASCADE)
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
    def total_venta(self):
        return self.producto.precio * self.cantidad

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField(choices=[(1, '1 persona'), (2, '2 personas'), (3, '3 personas'), (4, '4 personas'), (5, '5 o más personas')])

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

class Boleta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    nombre_usuario = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(max_length=15, choices=METODO_PAGO_OPCIONES)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True, related_name='boletas')

    def __str__(self):
        reserva_info = f" con reserva en {self.reserva.mesa}" if self.reserva else " sin reserva"
        return f"Boleta de {self.nombre_usuario} el {self.fecha_hora}{reserva_info}"

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    productos = models.ManyToManyField(Producto, related_name='menus')

    def __str__(self):
        return self.nombre

class ContactMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Mensaje de {self.user.username} el {self.created_at}"
        else:
            return f"Mensaje de {self.name} el {self.created_at}"

    def save(self, *args, **kwargs):
        if self.user:
            self.name = self.user.get_full_name()
            self.email = self.user.email
        super().save(*args, **kwargs)
