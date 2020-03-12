import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# Funciones para la generacion de pdfs de


# Full url para imagenes
# Retorna la ruta completa de la imagen a incluir en el pdf
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


# Renderizado de datos a pdf mediante libreria xhtml2pdf
def render_create_proyecto_to_pdf(data_render):
    template_path = 'proyecto_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None


def render_update_proyecto_to_pdf(data_render):
    template_path = 'proyecto_update.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_etapa_to_pdf(data_render):
    template_path = 'etapa_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode('UTF-8')),
        result,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_update_etapa_to_pdf(data_render):
    template_path = 'etapa_update.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_cotizacion_to_pdf(data_render, response):
    template_path = 'cotizacion_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        dest=response,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_pre_approbation_to_pdf(data_render, response):
    template_path = 'pre_approbation.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        dest=response,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None

def render_create_oferta_to_pdf(data_render):
    template_path = 'oferta_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        result,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_ficha_to_pdf(data_render):
    template_path = 'ficha_pre_aprobacion.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        result,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_simulador_to_pdf(data_render):
    template_path = 'simulador_credito.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        result,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_restrictions_to_pdf(data_render):
    template_path = 'restriction_inmueble_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_factura_to_pdf(data_render, response):
    template_path = 'factura_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        dest=response,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None


def render_create_nota_credito_to_pdf(data_render, response):
    template_path = 'nota_credito_add.html'
    html = render_to_string(template_path, data_render)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(
            html.encode('UTF-8')),
        dest=response,
        link_callback=link_callback)
    if not pdf.err:
        return result.getvalue()
    return None