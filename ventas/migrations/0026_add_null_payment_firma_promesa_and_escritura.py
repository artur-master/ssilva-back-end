# Generated by Django 2.1.2 on 2019-03-31 00:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0025_cliente_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='Extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='PaymentFirmaEscritura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='PaymentFirmaPromesa',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
