import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycafe.settings')

import django
django.setup()

from myappcafe.models import Producto

productos = [
    {"nombre": "Cappuccino", "descripcion": "Café espresso, leche vaporizada y espuma de leche.", "precio": 3200, "tipo": "CALIENTE"},
    {"nombre": "Caffe Latté", "descripcion": "Café espresso y una mayor cantidad de leche vaporizada con un poco de espuma de leche.", "precio": 2800, "tipo": "CALIENTE"},
    {"nombre": "Mocca", "descripcion": "Café espresso, chocolate, leche vaporizada y espuma de leche.", "precio": 3250, "tipo": "CALIENTE"},
    {"nombre": "Espresso", "descripcion": "Café concentrado y fuerte, preparado rápidamente con agua caliente a alta presión.", "precio": 2400, "tipo": "CALIENTE"},
    {"nombre": "Double", "descripcion": "Doble cantidad de café espresso.", "precio": 4000, "tipo": "CALIENTE"},
    {"nombre": "Americano", "descripcion": "Café espresso diluido con agua caliente.", "precio": 1800, "tipo": "CALIENTE"},
    {"nombre": "Flat White", "descripcion": "Café espresso con una capa delgada de leche vaporizada.", "precio": 3300, "tipo": "CALIENTE"},
    {"nombre": "Latte Macchiato", "descripcion": "Leche vaporizada con un toque de café espresso.", "precio": 3400, "tipo": "CALIENTE"},
    {"nombre": "Lungo", "descripcion": "Café espresso extraído durante más tiempo, resultando en una bebida más grande y menos concentrada.", "precio": 2900, "tipo": "CALIENTE"},
    {"nombre": "Ristretto", "descripcion": "Café espresso más concentrado y fuerte, con menos cantidad de agua.", "precio": 2050, "tipo": "CALIENTE"},
    {"nombre": "Frappuccino", "descripcion": "Una bebida helada y cremosa a base de café hecha con café instantáneo, leche, hielo y generalmente jarabe de vainilla y crema batida.", "precio": 2800, "tipo": "FRIA"},
    {"nombre": "Milk Shake", "descripcion": "Helado de vainilla, leche y café recién preparado, mezclado hasta obtener una textura suave.", "precio": 3600, "tipo": "FRIA"},
    {"nombre": "Iced Latte", "descripcion": "Un clásico refrescante hecho con espresso helado, leche fría y, a menudo, un toque de jarabe simple.", "precio": 3000, "tipo": "FRIA"},
    {"nombre": "Iced Mocha", "descripcion": "Similar a un Iced Latte, pero con la adición de chocolate o jarabe de chocolate para un sabor más dulce y decadente.", "precio": 3100, "tipo": "FRIA"},
    {"nombre": "Irish Coffee", "descripcion": "Café caliente con un toque de whisky irlandés, azúcar y crema batida (versión fría también disponible).", "precio": 4000, "tipo": "CALIENTE"},
    {"nombre": "Cold Brew Coffee", "descripcion": "Preparado con café molido empapado en agua fría durante un período prolongado, lo que produce una bebida suave y con menos acidez.", "precio": 3200, "tipo": "FRIA"},
    {"nombre": "Nitro Cold Brew", "descripcion": "Similar al Cold Brew Coffee, pero infundido con nitrógeno para una textura cremosa y similar a la cerveza.", "precio": 4000, "tipo": "FRIA"},
    {"nombre": "Iced Americano", "descripcion": "Espresso helado diluido con agua fría, perfecto para aquellos que disfrutan del sabor puro del café sin la leche.", "precio": 2000, "tipo": "FRIA"},
    {"nombre": "Iced Micchiato", "descripcion": "Similar a un Iced Latte, pero con una capa de espuma de leche en la parte superior para un contraste de texturas.", "precio": 3100, "tipo": "FRIA"},
    {"nombre": "Freddo Espresso", "descripcion": "Espresso helado vertido sobre una bola de helado, creando un postre refrescante y cafeinado.", "precio": 3700, "tipo": "FRIA"}
]

for producto in productos:
    Producto.objects.create(
        nombre=producto['nombre'],
        descripcion=producto['descripcion'],
        precio=producto['precio'],
        tipo=producto['tipo']
    )

print("Productos agregados exitosamente.")