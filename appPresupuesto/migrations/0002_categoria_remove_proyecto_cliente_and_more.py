# Generated by Django 5.1.3 on 2024-11-08 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appPresupuesto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='detallepresupuesto',
            name='material',
        ),
        migrations.RemoveField(
            model_name='detallepresupuesto',
            name='presupuesto',
        ),
        migrations.RemoveField(
            model_name='presupuesto',
            name='proyecto',
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appPresupuesto.categoria')),
            ],
        ),
        migrations.DeleteModel(
            name='Cliente',
        ),
        migrations.DeleteModel(
            name='Material',
        ),
        migrations.DeleteModel(
            name='DetallePresupuesto',
        ),
        migrations.DeleteModel(
            name='Presupuesto',
        ),
        migrations.DeleteModel(
            name='Proyecto',
        ),
    ]
