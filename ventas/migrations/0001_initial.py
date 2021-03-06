# Generated by Django 2.1.2 on 2020-02-27 15:28

import django.contrib.postgres.fields.jsonb
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
            name='Cliente',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.User')),
                ('Address', models.CharField(max_length=150)),
                ('CreationDate', models.DateTimeField(auto_now_add=True)),
                ('LastModificationDate', models.DateTimeField(auto_now=True)),
                ('Nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('Genre', models.CharField(blank=True, max_length=100, null=True)),
                ('BirthDate', models.DateField(blank=True, null=True)),
                ('CivilStatus', models.CharField(blank=True, max_length=100)),
                ('Ocupation', models.CharField(blank=True, max_length=100)),
                ('Position', models.CharField(blank=True, max_length=100)),
                ('Carga', models.PositiveSmallIntegerField(default=0)),
                ('Salary', models.PositiveIntegerField(default=0)),
                ('TotalPatrimony', models.PositiveIntegerField(default=0)),
                ('Antiquity', models.CharField(blank=True, max_length=100)),
                ('ContractMarriageType', models.CharField(blank=True, max_length=100)),
                ('IsDefinitiveResidence', models.BooleanField(default=False)),
                ('IsCompany', models.BooleanField(default=False)),
                ('Extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('GiroEmpresa', models.CharField(blank=True, max_length=250)),
                ('ReprenetanteLegal', models.CharField(blank=True, max_length=250)),
                ('ComunaID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comuna_cliente', to='common.Comuna')),
            ],
            bases=('users.user',),
        ),
        migrations.CreateModel(
            name='ClienteContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Value', models.CharField(max_length=60)),
                ('ContactInfoTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.ContactInfoType')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ClienteProyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ComisionInmobiliaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PromesaFirmada', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('EscrituraFirmada', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('CierreGestion', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('State', models.CharField(choices=[('to_confirm', 'To Confirm'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected')], default='to_confirm', max_length=50)),
                ('NoExisted', models.BooleanField(default=False)),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_comision_inmobiliaria', to='empresas_and_proyectos.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ConditionID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Description', models.CharField(blank=True, max_length=150, null=True)),
                ('IsImportant', models.BooleanField(default=False)),
                ('IsApprove', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMethodType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ContactMethodTypeID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CotizacionID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Folio', models.CharField(max_length=50)),
                ('IsNotInvestment', models.BooleanField(default=False)),
                ('DateFirmaPromesa', models.DateTimeField(blank=True, null=True)),
                ('PaymentFirmaPromesa', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('PaymentFirmaEscritura', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('PaymentInstitucionFinanciera', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('AhorroPlus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ClienteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_cotizacion', to='ventas.Cliente')),
                ('ContactMethodTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medio_contacto_cotizacion', to='ventas.ContactMethodType')),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('CotizacionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Cotizacion')),
                ('InmuebleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Inmueble')),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CotizacionStateID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CotizacionTypeID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CounterFolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Count', models.IntegerField(default=1)),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_contador', to='empresas_and_proyectos.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CuotaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Amount', models.DecimalField(decimal_places=10, max_digits=30)),
                ('Date', models.DateTimeField()),
                ('Observacion', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Folio', models.CharField(blank=True, max_length=50, null=True)),
                ('DocumentCotizacion', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentOferta', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentOfertaFirmada', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
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
                ('DocumentCertificadoSociedad', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentCarpetaTributaria', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentBalancesTimbrados', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('Document6IVA', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('Document2DAI', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentTituloProfesional', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentAcredittacionAhorros', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentAcredittacionDeudas', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
            ],
        ),
        migrations.CreateModel(
            name='Empleador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmpleadorID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Rut', models.CharField(blank=True, max_length=12, null=True)),
                ('RazonSocial', models.CharField(blank=True, max_length=150, null=True)),
                ('Extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('ClienteID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_empleador', to='ventas.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaCompradora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EmpresaCompradoraID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('RazonSocial', models.CharField(blank=True, max_length=150, null=True)),
                ('Rut', models.CharField(blank=True, max_length=12, null=True)),
                ('Address', models.CharField(blank=True, max_length=150, null=True)),
                ('ClienteID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_cliente', to='ventas.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FacturaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Number', models.IntegerField(blank=True, null=True)),
                ('Value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('DateEnvio', models.DateTimeField(blank=True, null=True)),
                ('DatePayment', models.DateTimeField(blank=True, null=True)),
                ('FacturaState', models.CharField(max_length=100)),
                ('Folio', models.CharField(blank=True, max_length=50, null=True)),
                ('InmobiliariaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inmobiliaria_factura', to='empresas_and_proyectos.Inmobiliaria')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FolioVenta', models.CharField(max_length=50)),
                ('Price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Comision', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Tipo', models.CharField(max_length=50)),
                ('State', models.CharField(max_length=50)),
                ('FacturaID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factura_factura_inmueble', to='ventas.Factura')),
                ('InmuebleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inmueble_factura_inmueble', to='empresas_and_proyectos.Inmueble')),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_factura_inmueble', to='empresas_and_proyectos.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='FindingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FindingTypeID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OfertaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Folio', models.CharField(max_length=50)),
                ('OfertaState', models.CharField(max_length=100)),
                ('AprobacionInmobiliariaState', models.CharField(max_length=100)),
                ('AprobacionInmobiliaria', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('PreAprobacionCreditoState', models.CharField(max_length=100)),
                ('RecepcionGarantiaState', models.CharField(max_length=100)),
                ('PaymentFirmaPromesa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PaymentFirmaEscritura', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PaymentInstitucionFinanciera', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('AhorroPlus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('DateFirmaPromesa', models.DateTimeField(blank=True, null=True)),
                ('ValueProductoFinanciero', models.IntegerField(blank=True, null=True)),
                ('IsApproveInmobiliaria', models.BooleanField(default=False)),
                ('ClienteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_oferta', to='ventas.Cliente')),
                ('CodeudorID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codeudor_oferta', to='ventas.Cliente')),
                ('ContactMethodTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medio_contacto_oferta', to='ventas.ContactMethodType')),
                ('CotizacionTypeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_cotizacion_oferta', to='ventas.CotizacionType')),
                ('EmpresaCompradoraID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_compradora_oferta', to='ventas.EmpresaCompradora')),
            ],
        ),
        migrations.CreateModel(
            name='Patrimony',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatrimonyID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('RealState', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('Vehicle', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('DownPayment', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('Other', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('CreditCard', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('CreditoConsumo', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('CreditoHipotecario', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('PrestamoEmpleador', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('CreditoComercio', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('DeudaIndirecta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('AnotherCredit', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('Deposits', models.FloatField(blank=True, default=0, null=True)),
                ('Rent', models.IntegerField(blank=True, default=0, null=True)),
                ('ClienteID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_patrimony', to='ventas.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='PayType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PayTypeID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PreAprobacionCredito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PreAprobacionCreditoID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('InstitucionFinanciera', models.CharField(max_length=100)),
                ('Date', models.DateField(blank=True, null=True)),
                ('Result', models.CharField(blank=True, max_length=100, null=True)),
                ('DocumentCredit', models.FileField(blank=True, null=True, upload_to='PreAprobacionCredito')),
                ('Observacion', models.CharField(max_length=300, null=True)),
                ('OfertaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferta_pre_aprobacion_credito', to='ventas.Oferta')),
            ],
        ),
        migrations.CreateModel(
            name='ProductoFinanciero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductoFinancieroID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=20)),
                ('Value', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Promesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PromesaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Folio', models.CharField(max_length=50)),
                ('PromesaState', models.CharField(max_length=200)),
                ('AprobacionInmobiliaria', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('PromesaDesistimientoState', models.CharField(blank=True, max_length=200, null=True)),
                ('PromesaResciliacionState', models.CharField(blank=True, max_length=200, null=True)),
                ('PromesaResolucionState', models.CharField(blank=True, max_length=200, null=True)),
                ('PromesaModificacionState', models.CharField(blank=True, max_length=200, null=True)),
                ('DocumentPromesa', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentPromesaFirma', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentChequesFirma', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentPlantaFirma', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentFirmaComprador', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentResciliacion', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentResciliacionFirma', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DocumentResolucion', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DateEnvioPromesa', models.DateTimeField(blank=True, null=True)),
                ('DateRegresoPromesa', models.DateTimeField(blank=True, null=True)),
                ('DateLegalizacionPromesa', models.DateTimeField(blank=True, null=True)),
                ('DateEnvioCopias', models.DateTimeField(blank=True, null=True)),
                ('PaymentFirmaPromesa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PaymentFirmaEscritura', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PaymentInstitucionFinanciera', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('AhorroPlus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('IsOfficial', models.BooleanField(default=True)),
                ('FechaFirmaDeEscritura', models.DateTimeField(blank=True, null=True)),
                ('FechaEntregaDeInmueble', models.DateTimeField(blank=True, null=True)),
                ('DateEnvioPromesaToCliente', models.DateTimeField(blank=True, null=True)),
                ('DesistimientoEspecial', models.CharField(blank=True, max_length=255, null=True)),
                ('ModificacionEnLaClausula', models.CharField(blank=True, max_length=255, null=True)),
                ('MetodoComunicacionEscrituracion', models.CharField(blank=True, max_length=255, null=True)),
                ('DocumentPaymentForm', models.FileField(blank=True, null=True, upload_to='DocumentVentas')),
                ('DatePayment', models.DateTimeField(blank=True, null=True)),
                ('ClienteID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_promesa', to='ventas.Cliente')),
                ('CodeudorID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codeudor_promesa', to='ventas.Cliente')),
                ('CotizacionTypeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_cotizacion_promesa', to='ventas.CotizacionType')),
            ],
        ),
        migrations.CreateModel(
            name='PromesaInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('InmuebleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Inmueble')),
                ('PromesaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Promesa')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ReservaID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('Folio', models.CharField(blank=True, max_length=50, null=True)),
                ('IsNotInvestment', models.BooleanField(default=False)),
                ('PaymentFirmaPromesa', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('PaymentFirmaEscritura', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('PaymentInstitucionFinanciera', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('AhorroPlus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('DateFirmaPromesa', models.DateTimeField(blank=True, null=True)),
                ('ValueProductoFinanciero', models.IntegerField(blank=True, null=True)),
                ('ClienteID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_reserva', to='ventas.Cliente')),
                ('CodeudorID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codeudor_reserva', to='ventas.Cliente')),
                ('ConditionID', models.ManyToManyField(blank=True, null=True, related_name='condition_reserva', to='ventas.Condition')),
                ('ContactMethodTypeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medio_contacto_reserva', to='ventas.ContactMethodType')),
                ('CotizacionTypeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_cotizacion_reserva', to='ventas.CotizacionType')),
                ('CuotaID', models.ManyToManyField(blank=True, null=True, related_name='cuota_reserva', to='ventas.Cuota')),
                ('EmpresaCompradoraID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_compradora_reserva', to='ventas.EmpresaCompradora')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaInmueble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('InmuebleID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Inmueble')),
                ('ReservaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Reserva')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ReservaStateID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Subsidio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubsidioID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Ahorro', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='VentaLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VentaLogID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('VentaID', models.UUIDField()),
                ('Folio', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('Comment', models.TextField(blank=True, null=True)),
                ('Date', models.DateTimeField(auto_now_add=True)),
                ('ClienteID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente_historial_venta', to='ventas.Cliente')),
                ('ProyectoID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_historial_venta', to='empresas_and_proyectos.Proyecto')),
                ('UserID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendedor_historial_venta', to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='VentaLogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VentaLogTypeID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('Name', models.CharField(max_length=60)),
                ('MaximunDays', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='ventalog',
            name='VentaLogTypeID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.VentaLogType'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='InmuebleID',
            field=models.ManyToManyField(blank=True, null=True, related_name='inmuebles_reserva', through='ventas.ReservaInmueble', to='empresas_and_proyectos.Inmueble'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='PayTypeID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tipo_pago_reserva', to='ventas.PayType'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_reserva', to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='ReservaStateID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estado_reserva', to='ventas.ReservaState'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='VendedorID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendedor_reserva', to='users.User'),
        ),
        migrations.AddField(
            model_name='promesa',
            name='InmuebleID',
            field=models.ManyToManyField(related_name='inmuebles_promesa', through='ventas.PromesaInmueble', to='empresas_and_proyectos.Inmueble'),
        ),
        migrations.AddField(
            model_name='promesa',
            name='PayTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipo_pago_promesa', to='ventas.PayType'),
        ),
        migrations.AddField(
            model_name='promesa',
            name='PromesaModified',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promesa_modificada', to='ventas.Promesa'),
        ),
        migrations.AddField(
            model_name='promesa',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_promesa', to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='promesa',
            name='VendedorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor_promesa', to='users.User'),
        ),
        migrations.AddField(
            model_name='oferta',
            name='PayTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipo_pago_oferta', to='ventas.PayType'),
        ),
        migrations.AddField(
            model_name='oferta',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_oferta', to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='oferta',
            name='VendedorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor_oferta', to='users.User'),
        ),
        migrations.AddField(
            model_name='factura',
            name='InmuebleID',
            field=models.ManyToManyField(related_name='inmuebles_factura', through='ventas.FacturaInmueble', to='empresas_and_proyectos.Inmueble'),
        ),
        migrations.AddField(
            model_name='factura',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_factura', to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='CotizacionStateID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estado_cotizacion', to='ventas.CotizacionState'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='CotizacionTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipo_cotizacion', to='ventas.CotizacionType'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='CotizadorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cotizador_cotizacion', to='users.User'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='CuotaID',
            field=models.ManyToManyField(related_name='cuotas_cotizacion', to='ventas.Cuota'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='InmuebleID',
            field=models.ManyToManyField(related_name='inmuebles_cotizacion', through='ventas.CotizacionInmueble', to='empresas_and_proyectos.Inmueble'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='PayType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paytype_cotizacion', to='ventas.PayType'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proyecto_cotizacion', to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='Vendedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendedor_cotizacion', to='users.User'),
        ),
        migrations.AddField(
            model_name='clienteproyecto',
            name='FindingTypeID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.FindingType'),
        ),
        migrations.AddField(
            model_name='clienteproyecto',
            name='ProyectoID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresas_and_proyectos.Proyecto'),
        ),
        migrations.AddField(
            model_name='clienteproyecto',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.Cliente'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='ContactInfo',
            field=models.ManyToManyField(related_name='contacto_cliente', through='ventas.ClienteContactInfo', to='common.ContactInfoType'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='Creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_cliente', to='users.User'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='LastModifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='last_modifier_cliente', to='users.User'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='Proyecto',
            field=models.ManyToManyField(related_name='finding_way', through='ventas.ClienteProyecto', to='empresas_and_proyectos.Proyecto'),
        ),
    ]
