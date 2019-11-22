# Generated by Django 2.1.2 on 2019-03-12 15:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0016_alter_date_add_auto_now_oferta'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreAprobacionCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PreAprobacionCreditoID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('InstitucionFinanciera', models.CharField(max_length=100)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Result', models.CharField(max_length=100)),
                ('OfertaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferta_pre_aprobacion_credito', to='ventas.Oferta')),
            ],
        ),
    ]
