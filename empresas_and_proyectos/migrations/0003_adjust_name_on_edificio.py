# Generated by Django 2.1.2 on 2019-02-28 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas_and_proyectos', '0002_remove_proyecto_morethanoneedificio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edificio',
            name='Name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
