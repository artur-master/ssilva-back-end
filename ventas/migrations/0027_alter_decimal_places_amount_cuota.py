# Generated by Django 2.1.2 on 2019-04-01 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0026_add_null_payment_firma_promesa_and_escritura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuota',
            name='Amount',
            field=models.DecimalField(decimal_places=10, max_digits=30),
        ),
    ]
