from django.db import models


class DocumentVenta(models.Model):
    Folio = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    DocumentCotizacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    
    DocumentOferta = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentOfertaFirmada = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
        
    DocumentFichaPreAprobacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentSimulador = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentCertificadoMatrimonio = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentConstitucionSociedad = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentPagoGarantia = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentFotocopiaCarnet = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentLiquidacion1 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentLiquidacion2 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentLiquidacion3 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentCotizacionAFP = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
        
    DocumentCertificadoSociedad = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentCarpetaTributaria = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)     
    DocumentBalancesTimbrados = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True) 
        
    Document6IVA = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    Document2DAI = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)     
    DocumentTituloProfesional = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentAcredittacionAhorros = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentAcredittacionDeudas = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)          
        
    def __str__(self):
        return 'Documentos Folio: %s' % (self.Folio)
