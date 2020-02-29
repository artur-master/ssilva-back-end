# Generated by Django 2.1.2 on 2020-02-27 15:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('users', '0001_initial'),
        ('empresas_and_proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Count', models.IntegerField(default=1)),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEdificio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EdificioID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalEtapa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EtapaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=40)),
                ('SalesStartDate', models.DateTimeField(blank=True, null=True)),
                ('EtapaStateID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_estado_etapa', to='empresas_and_proyectos.EtapaState')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InmuebleID', models.UUIDField(default=uuid.uuid4, editable=False, null=True)),
                ('Number', models.IntegerField()),
                ('Floor', models.IntegerField(blank=True, null=True)),
                ('BathroomQuantity', models.IntegerField(blank=True, null=True)),
                ('BedroomsQuantity', models.IntegerField(blank=True, null=True)),
                ('UtilSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TerraceSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('LodgeSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TotalSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('IsNotUsoyGoce', models.BooleanField(default=False)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('MaximunDiscount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('CotizacionDuration', models.IntegerField(blank=True, default=0, null=True)),
                ('EdificioID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_edificio_inmueble', to='history.HistoricalEdificio')),
                ('EtapaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_etapa_inmueble', to='history.HistoricalEtapa')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInmuebleInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InmuebleAID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_inmueble_inmueble_a', to='history.HistoricalInmueble')),
                ('InmuebleBID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_inmueble_inmueble_b', to='history.HistoricalInmueble')),
                ('InmuebleInmuebleTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.InmuebleInmuebleType')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HistoricalProyectoID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('ProyectoID', models.UUIDField()),
                ('Counter', models.IntegerField(default=0)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Name', models.CharField(max_length=150)),
                ('Arquitecto', models.CharField(blank=True, max_length=150, null=True)),
                ('Symbol', models.CharField(blank=True, max_length=20, null=True)),
                ('Address', models.CharField(blank=True, max_length=150, null=True)),
                ('CotizacionDuration', models.IntegerField(blank=True, null=True)),
                ('GuaranteeAmount', models.IntegerField(blank=True, null=True)),
                ('MoreThanOneEtapa', models.BooleanField(default=False)),
                ('BorradorPromesaState', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_estado_borrador_promesa_proyecto', to='empresas_and_proyectos.BorradorPromesaState')),
                ('ComunaID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_comuna_proyecto', to='common.Comuna')),
                ('ConstructoraID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_constructora_proyecto', to='empresas_and_proyectos.Constructora')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProyectoAseguradora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProyectoAseguradoraID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ExpirationDate', models.DateTimeField(blank=True, null=True)),
                ('AseguradoraID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Aseguradora')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalProyectoContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Value', models.CharField(max_length=60)),
                ('ContactInfoTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.ContactInfoType')),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.HistoricalProyecto')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalUserProyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.HistoricalProyecto')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
                ('UserProyectoTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.UserProyectoType')),
            ],
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='ContactInfo',
            field=models.ManyToManyField(related_name='historical_contacto_proyecto', through='history.HistoricalProyectoContactInfo', to='common.ContactInfoType'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='IngresoComisionesState',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_estado_ingreso_comisiones_proyecto', to='empresas_and_proyectos.IngresoComisionesState'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='InmobiliariaID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_inmobiliaria_proyecto', to='empresas_and_proyectos.Inmobiliaria'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='InstitucionFinancieraID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_institucion_financiera_proyecto', to='empresas_and_proyectos.InstitucionFinanciera'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='PlanMediosState',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_estado_plan_medios_proyecto', to='empresas_and_proyectos.PlanMediosState'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='ProyectoAseguradoraID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historical_aseguradora_proyecto', to='history.HistoricalProyectoAseguradora'),
        ),
        migrations.AddField(
            model_name='historicalproyecto',
            name='UserProyecto',
            field=models.ManyToManyField(related_name='historical_usuario_proyecto', through='history.HistoricalUserProyecto', to='users.User'),
        ),
        migrations.AddField(
            model_name='historicalinmueble',
            name='InmuebleRestrict',
            field=models.ManyToManyField(through='history.HistoricalInmuebleInmueble', to='history.HistoricalInmueble'),
        ),
        migrations.AddField(
            model_name='historicalinmueble',
            name='InmuebleStateID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_estado_inmueble', to='empresas_and_proyectos.InmuebleState'),
        ),
        migrations.AddField(
            model_name='historicalinmueble',
            name='InmuebleTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_tipo_inmueble', to='empresas_and_proyectos.InmuebleType'),
        ),
        migrations.AddField(
            model_name='historicalinmueble',
            name='OrientationID',
            field=models.ManyToManyField(related_name='historical_orientation_inmueble', to='empresas_and_proyectos.Orientation'),
        ),
        migrations.AddField(
            model_name='historicalinmueble',
            name='TipologiaID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historical_tipologia_inmueble', to='empresas_and_proyectos.Tipologia'),
        ),
        migrations.AddField(
            model_name='historicaletapa',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_proyecto_etapa', to='history.HistoricalProyecto'),
        ),
        migrations.AddField(
            model_name='historicaledificio',
            name='EtapaID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_etapa_edificio', to='history.HistoricalEtapa'),
        ),
    ]
