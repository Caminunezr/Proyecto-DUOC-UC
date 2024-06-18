from django.db import models

# Create your models here.
class Cafe(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Mesa(models.Model):
    Nombre = models.CharField(max_length=100)
    Cantperson=models.PositiveIntegerField()
    Fecha=models.DateField()
    Hora=models.TimeField()
    Descripcion = models.TextField()
    Disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"mesa reservada por {self.Nombre} para {self.Cantperson} personas"
    
class CustomUser(models.Model):
    Primer_Nombre = models.CharField(max_length=30)
    Segundo_Nombre = models.CharField(max_length=30)
    Email = models.EmailField(unique=True)
    Cumpleaños = models.DateField(null=True, blank=True)

    def _str_(self):
        return self.Email
    



