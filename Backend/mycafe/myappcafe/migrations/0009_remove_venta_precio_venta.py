# Generated by Django 5.0.6 on 2024-06-20 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myappcafe', '0008_alter_ingrediente_cantidad_en_stock_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='precio_venta',
        ),
    ]
