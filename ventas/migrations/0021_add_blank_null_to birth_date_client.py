# Generated by Django 2.1.2 on 2019-03-18 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0020_remove_fields_venta_log_add_model_document_venta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='BirthDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
