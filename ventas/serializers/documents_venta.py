from ventas.models.documents import DocumentVenta
from rest_framework import serializers
from common.services import get_full_path_x


class DocumentVentaSerializer(serializers.ModelSerializer):
    DocumentCotizacion = serializers.SerializerMethodField(
        'get_cotizacion_url')
    DocumentOferta = serializers.SerializerMethodField(
        'get_oferta_url')
    DocumentOfertaFirmada = serializers.SerializerMethodField(
        'get_oferta_firmada_url')    
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

    class Meta:
        model = DocumentVenta
        fields = ('DocumentCotizacion', 'DocumentOferta', 'DocumentOfertaFirmada', 'DocumentFichaPreAprobacion',
                  'DocumentSimulador', 'DocumentCertificadoMatrimonio', 'DocumentConstitucionSociedad',
                  'DocumentPagoGarantia', 'DocumentFotocopiaCarnet', 'DocumentLiquidacion1',
                  'DocumentLiquidacion2', 'DocumentLiquidacion3', 'DocumentCotizacionAFP',
                  'DocumentCertificadoSociedad', 'DocumentCarpetaTributaria', 'DocumentBalancesTimbrados',
                  'Document6IVA', 'Document2DAI', 'DocumentTituloProfesional', 
                  'DocumentAcredittacionAhorros', 'DocumentAcredittacionDeudas')

    def get_cotizacion_url(self, obj):
        if obj.DocumentCotizacion and hasattr(
                obj.DocumentCotizacion, 'url'):
            url = self.context.get('url')
            absolute_url = get_full_path_x(url)
            return "%s%s" % (absolute_url, obj.DocumentCotizacion.url)
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
