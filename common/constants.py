# Definicion de constantes globales 

API_UF_URL = 'https://mindicador.cl/api/uf/'

DATABASE_URL = 'postgres://postgres:postgres@127.0.0.1:5432/sgi_web'

PERMISSION_MESSAGE = "Error, no tienes los permisos correspondientes"

DEFAULT_ETAPA_NAME = "Inicial"

DEFAULT_BATCH_SIZE = 500
DEFAULT_PRECISION = 0.1

PERMISSIONS = [
    "Administra roles", "Administra usuarios", "Administra inmobiliarias",
    "Es representante inmobiliario", "Consulta roles", "Consulta usuarios",
    "Consulta inmobiliarias", "Es jefe de proyectos", "Es vendedor",
    "Es asistente comercial", "Consulta parámetros", "Administra parámetros",
    "Administra proyectos", "Aprueba proyectos", "Monitorea proyectos",
    "Es aprobador inmobiliario", "Consulta proyectos", "Administra clientes",
    "Consulta clientes", "Aprueba inmuebles", "Recepciona garantias",
    "Aprueba confeccion promesa", "Confecciona maquetas",
]

NOTIFICATION_TYPE = [
    "Inmobiliaria sin representante", "Proyecto sin representante", "Proyecto sin vendedor",
    "Proyecto sin asistente comercial", "Proyecto sin jefe de proyectos", "Proyecto requiere aprobación",
    "Proyecto aprobado", "Proyecto rechazado", "Cambio de contraseña pendiente", "Inmobiliaria sin aprobador",
    "Proyecto sin aprobador", "Etapa sin fecha de ventas", "Proyecto con instituci\u00f3n financiera pendiente",
    "Proyecto con aseguradora pendiente", "Proyecto pendiente a aprobación", "Proyecto con constructora pendiente",
    "Proyecto sin inmuebles", "Reserva con información pendiente", "Reserva con control pendiente",
    "Reserva rechazada", "Reserva cancelada", "Reserva modificada con información pendiente",
    "Reserva modificada con control pendiente", "Proyecto sin borrador de promesa",
    "Oferta creada", "Oferta requiere aprobacion inmobiliaria",
    "Oferta aprobada", "Oferta rechazada",
    "Preaprobacion credito aprobada", "Preaprobacion credito rechazada",
    "Oferta pendiente aprobacion confeccion promesa",
    "Oferta requiere aprobacion confeccion promesa",
    "Confeccion promesa aprobada", "Confeccion promesa rechazada",
    "Oferta cancelada", "Oferta modificada", "Promesa creada",
    "Maqueta aprobada", "Maqueta rechazada", "Promesa aprobada",
    "Promesa rechazada", "Promesa enviada a inmobiliaria",
    "Envio de copias", "Promesa modificada", "Documento confirmado", "Documento rechazado", "Documento de actualizacion",
    "Crear comision", "Comision de actualizacion"
]

PROYECTO_APPROVAL_STATE = [
    "Pendiente, falta información",
    "Pendiente, falta aprobación legal",
    "Pendiente, falta aprobación gerencia",
    "Aprobado",
]

PLAN_MEDIOS_STATE = [
    "Pendiente", "Agregado",
]

BORRADOR_PROMESA_STATE = [
    "Pendiente", "Agregado",
]

INGRESO_COMISIONES_STATE = [
    "Pendiente", "Agregado",
]

PROYECTO_LOG_TYPE = [
    "Creación", "Aprobación legal", "Modificación",
    "Modificación restricciones", "Cancelación", "Rechazo legal",
    "Confección Plan De Medios", "Confección Borrador Promesa",
    "Ingreso Comisiones", "Aprobación gerencia", "Rechazo gerencia",
    "Inicio de Ventas",
]

VENTA_LOG_TYPE = [
    "Creacion reserva", "Reserva a control",
    "Aprobacion reserva", "Rechazo reserva",
    "Cancelacion reserva", "Modificacion reserva",
    "Creacion oferta", "Envio aprobacion inmobiliaria",
    "Aprobacion oferta", "Rechazo oferta",
    "Recepcion garantia", "Envio oferta a confeccion promesa",
    "Aprobacion confeccion promesa", "Rechazo confeccion promesa",
    "Cancelacion oferta", "Modificacion oferta",
    "Creacion cotizacion", "Creacion promesa",
    "Aprobacion maqueta", "Rechazo maqueta",
    "Aprobacion promesa", "Rechazo promesa",
    "Registro envio promesa a inmobiliaria",
    "Registro firma de inmobiliaria",
    "Legalizacion promesa",
    "Envio copias",
    "Modificacion promesa(Antes de firma comprador)",
    "Modificacion promesa(Despues de firma comprador)",
]

USER_PROYECTO_TYPE = [
    "Representante", "Jefe de Proyecto",
    "Vendedor", "Asistente Comercial", "Aprobador",
    "Marketing", "Legal", "Finanza",
    "Autorizador", "Arquitecto"
]

USER_EMPRESA_TYPE = [
    "Representante", "Aprobador",
]

INMUEBLE_TYPE = [
    "Departamento", "Bodega", "Estacionamiento",
    "Casa",
]

INMUEBLE_STATE = [
    "Disponible", "Bloqueado por inmobiliaria",
    "Reservado", "Promesado", "Vendido",
]

COTIZATION_TYPE = [
    "Presencial", "No presencial",
]

COTIZATION_STATE = [
    "Vigente", "Vencida",
    "Reserva",
]

RESERVA_STATE = [
    "Pendiente información", "Pendiente control",
    "Oferta", "Rechazada", "Cancelada",
]

CONTACT_METHOD_TYPE = [
    "Portal inmobiliario", "Mail",
    "Teléfono", "Presencial",
]

FINDING_TYPE = [
    "No aplica",
]

SEARCH_NAME_CONSTANT_NUMERIC = [
    "tasa",
]

COMPANY_NAME = [
    "SGI Gestión Inmobiliaria S.A.",
    "SGI Corredores Asociados S.A",
]

ORIENTACIONES = [
    "No aplica", "Norte", "Nor-Oriente", "Nor-Poniente",
    "Norte-Sur", "Oriente", "Oriente-Poniente", "Poniente",
    "Sur", "Sur-Oriente", "Sur-Poniente", "Oriente-Nor-Poniente",
    "Norte-Oriente-Sur", "Norte-Poniente-Sur",
]

AREA_APPROVE = [
    "legal",
    "gerencia",
]

PAY_TYPE = [
    "Contado",
    "Credito",
]

GENRES = [
    "Masculino",
    "Femenino",
    "Otro",
]

CIVIL_STATUS = [
    "Soltero(a)", "Casado(a)", "Divorciado(a)",
    "Viudo(a)", "Unido Civilmente",
]

CONTRACT_MARRIAGE_TYPES = [
    "No aplica",
    "Sociedad Conyugal",
    "Mujer Art. 150",
    "Separación de Bienes",
]

NATIONALITIES_TYPES = [
    "Chilena",
    "Extranjero",
]

ANTIQUITIES = [
    "No aplica",
    "- 1 año",
    "1 año",
    "+ 1 año",
]

SALARY_RANK = [
    "- 1 millon",
    "1 millon",
    "+1 millon",
]

AGE_RANK = [
    "- 30 años",
    "30 años",
    "+ 30 años",
]

OFERTA_STATE = [
    "Pendiente aprobaciones",
    "Pendiente legal",
    "Rechazada por legal",
    "Promesa",
    "Cancelada",
]

APROBACION_INMOBILIARIA_STATE = [
    "Pendiente jefe de proyecto",
    "Pendiente aprobador inmobiliario",
    "Aprobada",
    "Rechazada",
]

PRE_APROBACION_CREDITO_STATE = [
    "No aplica",
    "Pendiente asistente comercial",
    "Aprobada",
    "Rechazada",
]

RECEPCION_GARANTIA_STATE = [
    "Pendiente recepcion en finanzas",
    "Aprobada",
]

RESULT = [
    "Aprobada",
    "Rechazada",
]

PROMESA_STATE = [
    "Pendiente confección",
    "Pendiente firma comprador",
    "Pendiente envío a inmobiliaria",
    "Pendiente control",
    "Pendiente firma inmobiliaria",
    "Pendiente legalizacion",
    "Pendiente envio de copias",
    "Pendiente escrituracion",
    "Escritura",
    "Pendiente aprobación de maqueta",
    "Promesa modificada",
]

ETAPA_STATE = [
    "En blanco",
    "En verde",
    "En escrituración",
    "Vendido",
    "Iniciando escrituración",
]

FACTURA_INMUEBLE_TYPE = [
    "Promesa",
    "Escritura",
    "Cierre de gestion",
]

FACTURA_INMUEBLE_STATE = [
    "Pendiente factura",
    "Facturado",
]

FACTURA_STATE = [
    "Pendiente pago",
    "Pagada",
]

COMISION_STATE = [
    "Pendiente pago",
    "Pagada",
]

PROMESA_FIRMADA_TYPE = [
    "Firma",
    "Modificacion",
    "Desistimiento",
]

PROMESA_FIRMADA_STATE = [
    "Pendiente Cierre",
    "Cerrada",
]


class Constant(object):
    @classmethod
    def values(cls):
        return [value for key, value in cls.__dict__.items()
                if not key.startswith("__") and not key.endswith("__")
                and type(value) in [str, int, float]]


class LegalDocumentTypes(Constant):
    COUNTER_WORD = 'counter_word'
    COUNTER_PDF = 'counter_pdf'
    CREDIT_WORD = 'credit_word'
    CREDIT_PDF = 'credit_pdf'
    COMPANY_WORD = 'company_word'
    COMPANY_PDF = 'company_pdf'
    BROKERAGE_CONTRACT = 'brokerage_contract'
    DOMAIN_CERTIFICATE = 'domain_certificate'
    COMPANY_DEED = 'company_deed'
    APPROVED_PRICE_LIST = 'approved_price_list'
    TITLE_FOLDER = 'title_folder'


class MarketingDocumentTypes(Constant):
    MARKETING_EXCEL = 'marketing_excel'
    MARKETING_PDF = 'marketing_pdf'


class DocumentState(Constant):
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    TO_CONFIRM = 'to_confirm'


class UserRole(Constant):
    GERENTE_COMERCIAL = "Gerente Comercial"
    JEFE_DE_PROYECTO = "Jefe de Proyecto"
    ASISTENTE_COMERCIAL = "Asistente Comercial"
    VENDEDOR = "Vendedor"
    INMOBILIARIO = "Inmobiliario"
    ADMINISTRADOR = "Administrador"
    LEGAL = "Legal"
    ARQUITECTO = "Arquitecto"
    FINANZAS = "Finanzas"
    MARKETING = "Marketing"


FILE_NON_EXISTED = 'no_existed'
