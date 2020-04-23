from ventas.models.documents import DocumentVenta
from rest_framework import serializers
from common.services import get_full_path_x


class DocumentVentaSerializer(serializers.ModelSerializer):
    DocumentCotizacion = serializers.SerializerMethodField(
        'get_cotizacion_url')
    DocumentFirmadoCotizacion = serializers.SerializerMethodField(
        'get_firmadocotizacion_url')
    DocumentFirmadoCheques = serializers.SerializerMethodField(
        'get_firmadocheques_url')
    DocumentFirmadoSimulador = serializers.SerializerMethodField(
        'get_firmadosimulador_url')
    DocumentFirmadoFichaPreAprobacion = serializers.SerializerMethodField(
        'get_firmadoficha_url')
    DocumentOferta = serializers.SerializerMethodField(
        'get_oferta_url')
    DocumentOfertaFirmada = serializers.SerializerMethodField(
        'get_oferta_firmada_url')    
    DocumentPlanoFirmada = serializers.SerializerMethodField(
        'get_plano_firmada_url')    
    DocumentFichaPreAprobacion = serializers.SerializerMethodField(
        'get_ficha_url')
    DocumentSimulador = serializers.SerializerMethodField(
        'get_simulador_url')
    DocumentCertificadoMatrimonio = serializers.SerializerMethodField(
        'get_certificado_matrimonio_url')
    DocumentConstitucionSociedad = serializers.SerializerMethodField(
        'get_consitucion_sociedad_url')
    DocumentPagoGarantia = serializers.SerializerMethodField(
        'get_pago_garantia_url')
    DocumentFotocopiaCarnet = serializers.SerializerMethodField(
        'get_fotocopia_carnet_url')
    DocumentPreApprobation = serializers.SerializerMethodField(
        'get_pre_approbation_url')
    DocumentLiquidacion1 = serializers.SerializerMethodField(
        'get_liquidacion_1_url')
    DocumentLiquidacion2 = serializers.SerializerMethodField(
        'get_liquidacion_2_url')
    DocumentLiquidacion3 = serializers.SerializerMethodField(
        'get_liquidacion_3_url')
    DocumentCotizacionAFP = serializers.SerializerMethodField(
        'get_cotizacion_afp_url')
        
    DocumentCertificadoSociedad = serializers.SerializerMethodField(
        'get_DocumentCertificadoSociedad_url')
    DocumentCarpetaTributaria = serializers.SerializerMethodField(
        'get_DocumentCarpetaTributaria_url')   
    DocumentBalancesTimbrados = serializers.SerializerMethodField(
        'get_DocumentBalancesTimbrados_url') 
        
    Document6IVA = serializers.SerializerMethodField(
        'get_Document6IVA_url')
    Document2DAI = serializers.SerializerMethodField(
        'get_Document2DAI_url')   
    DocumentTituloProfesional = serializers.SerializerMethodField(
        'get_DocumentTituloProfesional_url')
    DocumentAcredittacionAhorros = serializers.SerializerMethodField(
        'get_DocumentAcredittacionAhorros_url')
    DocumentAcredittacionDeudas = serializers.SerializerMethodField(
        'get_DocumentAcredittacionDeudas_url')   

    #Codeudor
    
    DocumentCodeudorFirmadoCheques = serializers.SerializerMethodField(
        'get_DocumentCodeudorFirmadoCheques_url')   
    DocumentCodeudorFichaPreAprobacion = serializers.SerializerMethodField(
        'get_DocumentCodeudorFichaPreAprobacion_url')   
    DocumentCodeudorSimulador = serializers.SerializerMethodField(
        'get_DocumentCodeudorSimulador_url')   
    DocumentCodeudorCotizacion = serializers.SerializerMethodField(
        'get_DocumentCodeudorCotizacion_url')   
    DocumentCodeudorCertificadoMatrimonio = serializers.SerializerMethodField(
        'get_DocumentCodeudorCertificadoMatrimonio_url')   
    DocumentCodeudorFirmadoSimulador = serializers.SerializerMethodField(
        'get_DocumentCodeudorFirmadoSimulador_url')   
    DocumentCodeudorConstitucionSociedad = serializers.SerializerMethodField(
        'get_DocumentCodeudorConstitucionSociedad_url')   
    DocumentCodeudorCertificadoSociedad = serializers.SerializerMethodField(
        'get_DocumentCodeudorCertificadoSociedad_url')   
    DocumentCodeudorCarpetaTributaria = serializers.SerializerMethodField(
        'get_DocumentCodeudorCarpetaTributaria_url')   
    DocumentCodeudorBalancesTimbrados = serializers.SerializerMethodField(
        'get_DocumentCodeudorBalancesTimbrados_url')   
    Document6IVACodeudor = serializers.SerializerMethodField(
        'get_Document6IVACodeudor_url')   
    Document2DAICodeudor = serializers.SerializerMethodField(
        'get_Document2DAICodeudor_url')   
    DocumentCodeudorTituloProfesional = serializers.SerializerMethodField(
        'get_DocumentCodeudorTituloProfesional_url')   
    DocumentCodeudorAcredittacionAhorros = serializers.SerializerMethodField(
        'get_DocumentCodeudorAcredittacionAhorros_url')   
    DocumentCodeudorAcredittacionDeudas = serializers.SerializerMethodField(
        'get_DocumentCodeudorAcredittacionDeudas_url')   
    DocumentCodeudorFotocopiaCarnet = serializers.SerializerMethodField(
        'get_DocumentCodeudorFotocopiaCarnet_url')   
    DocumentCodeudorLiquidacion1 = serializers.SerializerMethodField(
        'get_DocumentCodeudorLiquidacion1_url')   
    DocumentCodeudorLiquidacion2 = serializers.SerializerMethodField(
        'get_DocumentCodeudorLiquidacion2_url')   
    DocumentCodeudorLiquidacion3 = serializers.SerializerMethodField(
        'get_DocumentCodeudorLiquidacion3_url')   

    class Meta:
        model = DocumentVenta
        fields = ('DocumentCotizacion', 'DocumentFirmadoCotizacion', 'DocumentFirmadoCheques',                                         
                  'DocumentFirmadoSimulador', 'DocumentFirmadoFichaPreAprobacion', 
                  'DocumentOferta', 'DocumentOfertaFirmada', 'DocumentPlanoFirmada', 'DocumentFichaPreAprobacion',
                  'DocumentSimulador', 'DocumentCertificadoMatrimonio', 'DocumentConstitucionSociedad',
                  'DocumentPagoGarantia', 'DocumentFotocopiaCarnet', 'DocumentPreApprobation', 'DocumentLiquidacion1',
                  'DocumentLiquidacion2', 'DocumentLiquidacion3', 'DocumentCotizacionAFP',
                  'DocumentCertificadoSociedad', 'DocumentCarpetaTributaria', 'DocumentBalancesTimbrados',
                  'Document6IVA', 'Document2DAI', 'DocumentTituloProfesional', 
                  'DocumentAcredittacionAhorros', 'DocumentAcredittacionDeudas',
                  'DocumentCodeudorFirmadoCheques','DocumentCodeudorFichaPreAprobacion',
                  'DocumentCodeudorSimulador','DocumentCodeudorCotizacion',
                  'DocumentCodeudorCertificadoMatrimonio','DocumentCodeudorFirmadoSimulador',
                  'DocumentCodeudorConstitucionSociedad','DocumentCodeudorCertificadoSociedad',
                  'DocumentCodeudorCarpetaTributaria','DocumentCodeudorBalancesTimbrados',
                  'Document6IVACodeudor','Document2DAICodeudor',
                  'DocumentCodeudorTituloProfesional','DocumentCodeudorAcredittacionAhorros',
                  'DocumentCodeudorAcredittacionDeudas','DocumentCodeudorFotocopiaCarnet',
                  'DocumentCodeudorLiquidacion1','DocumentCodeudorLiquidacion2',
                  'DocumentCodeudorLiquidacion3',)

    def get_cotizacion_url(self, obj):
        if obj.DocumentCotizacion and hasattr(
                obj.DocumentCotizacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCotizacion.url)
        else:
            return ""

    def get_firmadocotizacion_url(self, obj):
        if obj.DocumentFirmadoCotizacion and hasattr(
                obj.DocumentFirmadoCotizacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFirmadoCotizacion.url)
        else:
            return ""

    def get_firmadocheques_url(self, obj):
        if obj.DocumentFirmadoCheques and hasattr(
                obj.DocumentFirmadoCheques, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFirmadoCheques.url)
        else:
            return ""

    def get_firmadosimulador_url(self, obj):
        if obj.DocumentFirmadoSimulador and hasattr(
                obj.DocumentFirmadoSimulador, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFirmadoSimulador.url)
        else:
            return ""
            
    def get_firmadoficha_url(self, obj):
        if obj.DocumentFirmadoFichaPreAprobacion and hasattr(
                obj.DocumentFirmadoFichaPreAprobacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFirmadoFichaPreAprobacion.url)
        else:
            return ""

    def get_oferta_url(self, obj):
        if obj.DocumentOferta and hasattr(
                obj.DocumentOferta, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentOferta.url)
        else:
            return ""
    
    def get_oferta_firmada_url(self, obj):
        if obj.DocumentOfertaFirmada and hasattr(
                obj.DocumentOfertaFirmada, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentOfertaFirmada.url)
        else:
            return ""

    def get_plano_firmada_url(self, obj):
        if obj.DocumentPlanoFirmada and hasattr(
                obj.DocumentPlanoFirmada, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentPlanoFirmada.url)
        else:
            return ""
    
    def get_ficha_url(self, obj):
        if obj.DocumentFichaPreAprobacion and hasattr(
                obj.DocumentFichaPreAprobacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFichaPreAprobacion.url)
        else:
            return ""

    def get_simulador_url(self, obj):
        if obj.DocumentSimulador and hasattr(
                obj.DocumentSimulador, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentSimulador.url)
        else:
            return ""

    def get_certificado_matrimonio_url(self, obj):
        if obj.DocumentCertificadoMatrimonio and hasattr(
                obj.DocumentCertificadoMatrimonio, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCertificadoMatrimonio.url)
        else:
            return ""

    def get_consitucion_sociedad_url(self, obj):
        if obj.DocumentConstitucionSociedad and hasattr(
                obj.DocumentConstitucionSociedad, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentConstitucionSociedad.url)
        else:
            return ""

    def get_pago_garantia_url(self, obj):
        if obj.DocumentPagoGarantia and hasattr(
                obj.DocumentPagoGarantia, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentPagoGarantia.url)
        else:
            return ""

    def get_fotocopia_carnet_url(self, obj):
        if obj.DocumentFotocopiaCarnet and hasattr(
                obj.DocumentFotocopiaCarnet, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentFotocopiaCarnet.url)
        else:
            return ""

    def get_pre_approbation_url(self, obj):
        if obj.DocumentPreApprobation and hasattr(
                obj.DocumentPreApprobation, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentPreApprobation.url)
        else:
            return ""

    def get_liquidacion_1_url(self, obj):
        if obj.DocumentLiquidacion1 and hasattr(
                obj.DocumentLiquidacion1, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentLiquidacion1.url)
        else:
            return ""

    def get_liquidacion_2_url(self, obj):
        if obj.DocumentLiquidacion2 and hasattr(
                obj.DocumentLiquidacion2, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentLiquidacion2.url)
        else:
            return ""

    def get_liquidacion_3_url(self, obj):
        if obj.DocumentLiquidacion3 and hasattr(
                obj.DocumentLiquidacion3, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentLiquidacion3.url)
        else:
            return ""

    def get_cotizacion_afp_url(self, obj):
        if obj.DocumentCotizacionAFP and hasattr(
                obj.DocumentCotizacionAFP, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCotizacionAFP.url)
        else:
            return ""


    def get_DocumentCertificadoSociedad_url(self, obj):
        if obj.DocumentCertificadoSociedad and hasattr(
                obj.DocumentCertificadoSociedad, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCertificadoSociedad.url)
        else:
            return ""
    def get_DocumentCarpetaTributaria_url(self, obj):
        if obj.DocumentCarpetaTributaria and hasattr(
                obj.DocumentCarpetaTributaria, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCarpetaTributaria.url)
        else:
            return ""
    def get_DocumentBalancesTimbrados_url(self, obj):
        if obj.DocumentBalancesTimbrados and hasattr(
                obj.DocumentBalancesTimbrados, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentBalancesTimbrados.url)
        else:
            return ""   

    def get_Document6IVA_url(self, obj):
        if obj.Document6IVA and hasattr(
                obj.Document6IVA, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.Document6IVA.url)
        else:
            return ""
    def get_Document2DAI_url(self, obj):
        if obj.Document2DAI and hasattr(
                obj.Document2DAI, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.Document2DAI.url)
        else:
            return ""
    def get_DocumentTituloProfesional_url(self, obj):
        if obj.DocumentTituloProfesional and hasattr(
                obj.DocumentTituloProfesional, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentTituloProfesional.url)
        else:
            return ""     

    def get_DocumentAcredittacionAhorros_url(self, obj):
        if obj.DocumentAcredittacionAhorros and hasattr(
                obj.DocumentAcredittacionAhorros, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentAcredittacionAhorros.url)
        else:
            return ""
    def get_DocumentAcredittacionDeudas_url(self, obj):
        if obj.DocumentAcredittacionDeudas and hasattr(
                obj.DocumentAcredittacionDeudas, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentAcredittacionDeudas.url)
        else:
            return ""               
    # Codeudor
    def get_DocumentCodeudorFirmadoCheques_url(self, obj):
        if obj.DocumentCodeudorFirmadoCheques and hasattr(
                obj.DocumentCodeudorFirmadoCheques, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorFirmadoCheques.url)
        else:
            return ""               
    def get_DocumentCodeudorFichaPreAprobacion_url(self, obj):
        if obj.DocumentCodeudorFichaPreAprobacion and hasattr(
                obj.DocumentCodeudorFichaPreAprobacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorFichaPreAprobacion.url)
        else:
            return ""               
    def get_DocumentCodeudorSimulador_url(self, obj):
        if obj.DocumentCodeudorSimulador and hasattr(
                obj.DocumentCodeudorSimulador, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorSimulador.url)
        else:
            return ""               
    def get_DocumentCodeudorCotizacion_url(self, obj):
        if obj.DocumentCodeudorCotizacion and hasattr(
                obj.DocumentCodeudorCotizacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorCotizacion.url)
        else:
            return ""               
    def get_DocumentCodeudorCertificadoMatrimonio_url(self, obj):
        if obj.DocumentCodeudorCertificadoMatrimonio and hasattr(
                obj.DocumentCodeudorCertificadoMatrimonio, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorCertificadoMatrimonio.url)
        else:
            return ""               
    def get_DocumentCodeudorFirmadoSimulador_url(self, obj):
        if obj.DocumentCodeudorFirmadoSimulador and hasattr(
                obj.DocumentCodeudorFirmadoSimulador, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorFirmadoSimulador.url)
        else:
            return ""               
    def get_DocumentCodeudorConstitucionSociedad_url(self, obj):
        if obj.DocumentCodeudorConstitucionSociedad and hasattr(
                obj.DocumentCodeudorConstitucionSociedad, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorConstitucionSociedad.url)
        else:
            return ""               
    def get_DocumentCodeudorCertificadoSociedad_url(self, obj):
        if obj.DocumentCodeudorCertificadoSociedad and hasattr(
                obj.DocumentCodeudorCertificadoSociedad, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorCertificadoSociedad.url)
        else:
            return ""               
    def get_DocumentCodeudorCarpetaTributaria_url(self, obj):
        if obj.DocumentCodeudorCarpetaTributaria and hasattr(
                obj.DocumentCodeudorCarpetaTributaria, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorCarpetaTributaria.url)
        else:
            return ""               
    def get_DocumentCodeudorBalancesTimbrados_url(self, obj):
        if obj.DocumentCodeudorBalancesTimbrados and hasattr(
                obj.DocumentCodeudorBalancesTimbrados, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorBalancesTimbrados.url)
        else:
            return ""               
    def get_Document6IVACodeudor_url(self, obj):
        if obj.Document6IVACodeudor and hasattr(
                obj.Document6IVACodeudor, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.Document6IVACodeudor.url)
        else:
            return ""               
    def get_Document2DAICodeudor_url(self, obj):
        if obj.Document2DAICodeudor and hasattr(
                obj.Document2DAICodeudor, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.Document2DAICodeudor.url)
        else:
            return ""               
    def get_DocumentCodeudorTituloProfesional_url(self, obj):
        if obj.DocumentCodeudorTituloProfesional and hasattr(
                obj.DocumentCodeudorTituloProfesional, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorTituloProfesional.url)
        else:
            return ""               
    def get_DocumentCodeudorAcredittacionAhorros_url(self, obj):
        if obj.DocumentCodeudorAcredittacionAhorros and hasattr(
                obj.DocumentCodeudorAcredittacionAhorros, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorAcredittacionAhorros.url)
        else:
            return ""               
    def get_DocumentCodeudorAcredittacionDeudas_url(self, obj):
        if obj.DocumentCodeudorAcredittacionDeudas and hasattr(
                obj.DocumentCodeudorAcredittacionDeudas, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorAcredittacionDeudas.url)
        else:
            return ""               
    def get_DocumentCodeudorFotocopiaCarnet_url(self, obj):
        if obj.DocumentCodeudorFotocopiaCarnet and hasattr(
                obj.DocumentCodeudorFotocopiaCarnet, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorFotocopiaCarnet.url)
        else:
            return ""               
    def get_DocumentCodeudorLiquidacion1_url(self, obj):
        if obj.DocumentCodeudorLiquidacion1 and hasattr(
                obj.DocumentCodeudorLiquidacion1, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorLiquidacion1.url)
        else:
            return ""               
    def get_DocumentCodeudorLiquidacion2_url(self, obj):
        if obj.DocumentCodeudorLiquidacion2 and hasattr(
                obj.DocumentCodeudorLiquidacion2, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorLiquidacion2.url)
        else:
            return ""               
    def get_DocumentCodeudorLiquidacion3_url(self, obj):
        if obj.DocumentCodeudorLiquidacion3 and hasattr(
                obj.DocumentCodeudorLiquidacion3, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCodeudorLiquidacion3.url)
        else:
            return ""               
            
