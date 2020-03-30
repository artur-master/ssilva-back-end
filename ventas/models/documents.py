from django.db import models


class DocumentVenta(models.Model):
    Folio = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    DocumentCotizacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
    DocumentFirmadoCheques = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)
        
    DocumentFirmadoSimulador = models.FileField(
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
    DocumentPreApprobation = models.FileField(
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

    #Codeudor
    DocumentCodeudorFirmadoCheques = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorFichaPreAprobacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorSimulador = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorCotizacion = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorCertificadoMatrimonio = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorFirmadoSimulador = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorConstitucionSociedad = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorCertificadoSociedad = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorCarpetaTributaria = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorBalancesTimbrados = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    Document6IVACodeudor = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    Document2DAICodeudor = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorTituloProfesional = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorAcredittacionAhorros = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorAcredittacionDeudas = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorFotocopiaCarnet = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorLiquidacion1 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorLiquidacion2 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
    DocumentCodeudorLiquidacion3 = models.FileField(
        upload_to="DocumentVentas", null=True, blank=True)  
            
        
    def __str__(self):
        return 'Documentos Folio: %s' % (self.Folio)
