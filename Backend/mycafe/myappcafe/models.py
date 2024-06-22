from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

# Opciones para las unidades de medida
UNIDAD_MEDIDA_OPCIONES = (
    ('G', 'gramos'),
    ('Kg', 'kilogramos'),
    ('L', 'litros'),
    ('Ml', 'mililitros'),
)

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

            for receta in self.recetas.all():
                receta.ingrediente.cantidad_en_stock -= receta.cantidad_necesaria * Decimal(cantidad)
                receta.ingrediente.save()
        else:
            if self.cantidad_en_stock < cantidad:
                raise ValueError("Stock insuficiente para completar la venta.")
            self.cantidad_en_stock -= cantidad

        self.actualizar_disponibilidad()

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_en_stock = models.DecimalField(max_digits=9, decimal_places=2)
    unidad_medida = models.CharField(max_length=10, choices=UNIDAD_MEDIDA_OPCIONES, default='g')

    def __str__(self):
        return self.nombre

@receiver(post_save, sender=Ingrediente)
def update_product_availability(sender, instance, **kwargs):
    recetas = instance.receta_set.all()
    for receta in recetas:
        producto = receta.producto
        producto.actualizar_disponibilidad()
        producto.save()

class Receta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad_necesaria = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad_necesaria} {self.ingrediente.unidad_medida} de {self.ingrediente.nombre} para {self.producto.nombre}"

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fecha_hora = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} vendido/s el {self.fecha_hora}"

    @property
    def total_venta(self):
        return self.producto.precio * Decimal(self.cantidad)
