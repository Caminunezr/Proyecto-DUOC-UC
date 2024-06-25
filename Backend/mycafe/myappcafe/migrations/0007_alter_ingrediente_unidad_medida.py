# Generated by Django 5.0.6 on 2024-06-20 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappcafe', '0006_alter_ingrediente_unidad_medida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='unidad_medida',
            field=models.CharField(choices=[('G', 'gramos'), ('Kg', 'kilogramos'), ('L', 'litros'), ('Ml', 'mililitros')], default='g', max_length=10),
        ),
    ]
