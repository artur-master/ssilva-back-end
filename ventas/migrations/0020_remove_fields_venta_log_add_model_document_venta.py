# Generated by Django 2.1.2 on 2019-03-14 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0019_oferta_isapproveinmobiliaria'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Folio', models.CharField(max_length=50)),
                ('DocumentCotizacion', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentOferta', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentFichaPreAprobacion', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentSimulador', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentCertificadoMatrimonio', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentConstitucionSociedad', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentPagoGarantia', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentFotocopiaCarnet', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentLiquidacion1', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentLiquidacion2', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentLiquidacion3', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentCotizacionAFP', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
            ],
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentCertificadoMatrimonio',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentConstitucionSociedad',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentCotizacion',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentCotizacionAFP',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentFichaPreAprobacion',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentFotocopiaCarnet',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentLiquidacion1',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentLiquidacion2',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentLiquidacion3',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentOferta',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentPagoGarantia',
        ),
        migrations.RemoveField(
            model_name='ventalog',
            name='DocumentSimulador',
        ),
    ]
