# Definicion de constantes globales 

API_UF_URL = 'https://mindicador.cl/api/uf/'

DATABASE_URL = 'postgres://postgres:postgres@127.0.0.1:5432/sgi_web'

PERMISSION_MESSAGE = "Error, no tienes los permisos correspondientes"

DEFAULT_ETAPA_NAME = "Inicial"

DEFAULT_BATCH_SIZE = 500
DEFAULT_PRECISION = 0.1

PERMISSIONS = [
    "Administra roles",
    "Administra usuarios",
    "Administra inmobiliarias",
    "Es representante inmobiliario",
    "Consulta roles",
    "Consulta usuarios",
    "Consulta inmobiliarias", "Es jefe de proyectos", "Es vendedor",
    "Es asistente comercial", "Consulta parámetros", "Administra parámetros",
    "Administra proyectos", "Aprueba proyectos", "Monitorea proyectos",
    "Es aprobador inmobiliario", "Consulta proyectos", "Administra clientes",
    "Consulta clientes", "Aprueba inmuebles", "Recepciona garantias",
    "Aprueba confeccion promesa", "Confecciona maquetas",
]

NOTIFICATION_TYPE = [
    "Inmobiliaria sin representante", "Proyecto sin representante", "Proyecto sin vendedor",  # 2
    "Proyecto sin asistente comercial", "Proyecto sin jefe de proyectos", "Proyecto requiere aprobación",  # 5
    "Proyecto aprobado", "Proyecto rechazado", "Cambio de contraseña pendiente", "Inmobiliaria sin aprobador",  # 9
    "Proyecto sin aprobador", "Etapa sin fecha de ventas", "Proyecto con instituci\u00f3n financiera pendiente",  # 12
    "Proyecto con aseguradora pendiente", "Proyecto pendiente a aprobación", "Proyecto con constructora pendiente",
    # 15
    "Proyecto sin inmuebles", "Reserva con información pendiente", "Reserva con control pendiente",  # 18
    "Reserva rechazada", "Reserva cancelada", "Reserva modificada con información pendiente",  # 21
    "Reserva modificada con control pendiente", "Proyecto sin borrador de promesa",  # 23
    "Oferta creada", "Oferta requiere aprobacion inmobiliaria",
    "Oferta aprobada", "Oferta rechazada",
    "Preaprobacion credito aprobada", "Preaprobacion credito rechazada",
    "Oferta pendiente aprobacion confeccion promesa",  # 30
    "Oferta requiere aprobacion confeccion promesa",
    "Confeccion promesa aprobada", "Confeccion promesa rechazada",
    "Oferta cancelada", "Oferta modificada", "Promesa creada",  # 36
    "Maqueta aprobada", "Maqueta rechazada", "Promesa aprobada",  # 39
    "Promesa rechazada", "Promesa enviada a inmobiliaria",  # 41
    "Envio de copias", "Promesa modificada", "Documento confirmado", "Documento rechazado",
    "Documento de actualizacion",
    "Crear comision", "Comision de actualizacion",  # 48
    "Rechazo Modificacion oferta", "Aprobacion Modificacion oferta",
    "Refund garantia",  # 51
    "Maqueta aprobada - AC",  # 52
    "Promesa requiere revisión a negociación",  # 53
    "Promesa requiere aprobacion inmobiliaria a negociación",  # 54
    "Aprobacion negociación",  # 55
    "Rechazo negociación",  # 56
    "Pendiente aprobacion desistimiento",  # 57
    "Aprobacion desistimiento",  # 58
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
    "Creacion reserva",
    "Reserva a control",
    "Aprobacion reserva",
    "Rechazo reserva",
    "Cancelacion reserva",
    "Modificacion reserva",
    "Creacion oferta",
    "Envio aprobacion inmobiliaria",
    "Aprobacion oferta",
    "Rechazo oferta",  # 9
    "Recepcion garantia",
    "Envio oferta a confeccion promesa",
    "Aprobacion confeccion promesa",
    "Rechazo confeccion promesa",
    "Cancelacion oferta",
    "Modificacion oferta",
    "Creacion cotizacion",
    "Creacion promesa",
    "Aprobacion maqueta",
    "Rechazo maqueta",  # 19
    "Aprobacion promesa",
    "Rechazo promesa",
    "Registro envio promesa a inmobiliaria",
    "Registro firma de inmobiliaria",
    "Legalizacion promesa",  # 24
    "Envio copias",
    "Modificacion promesa(Antes de firma comprador)",
    "Modificacion promesa(Despues de firma comprador)",
    "Rechazo Modificacion oferta",
    "Aprobacion Modificacion oferta",
    "Aprobacion Modificacion oferta",
    "Refund garantia",  # 31
    "AC Aprobacion maqueta",  # 32
    "Envio a negociación",  # 33
    "Envio negociación a inmobiliaria",  # 34
    "Aprobacion a negociación",  # 35
    "Rechazo a negociación",  # 36
    "Register Desistimiento",  # 37
    "Aprobacion Desistimiento",  # 38
    "Envío promesa a cliente", #39
]

VENTA_LOG_TYPE_PROMESA = [
    "Envio oferta a confeccion promesa",
    "Aprobacion confeccion promesa",
    "Rechazo confeccion promesa",
    "Creacion promesa",
    "Aprobacion maqueta",
    "Rechazo maqueta",  # 19
    "Aprobacion promesa",
    "Rechazo promesa",
    "Registro envio promesa a inmobiliaria",
    "Registro firma de inmobiliaria",
    "Legalizacion promesa",  # 24
    "Envio copias",
    "Modificacion promesa(Antes de firma comprador)",
    "Modificacion promesa(Despues de firma comprador)",
    "AC Aprobacion maqueta",  # 31
    "Envio a negociación",  # 32
    "Envio negociación a inmobiliaria",  # 33
    "Aprobacion a negociación",  # 34
    "Rechazo a negociación",  # 35
    "Register Desistimiento",  # 36
    "Aprobacion Desistimiento",  # 37
    "Envío promesa a cliente",
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
    "Modificado"
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
    "Refund",
]

RESULT = [
    "Aprobada",
    "Rechazada",
]

PROMESA_STATE = [
    "Pendiente confección",  # 0 -> 9
    "Pendiente firma comprador",  # 1 -> 20 or 13
    "Pendiente envío a inmobiliaria",  # 2 -> 3
    "Pendiente factura",  # 3 -> 4
    "Pendiente firma inmobiliaria",  # 4 -> 5 or 6
    "Pendiente legalizacion",  # 5 -> 6
    "Pendiente envio de copias",  # 6 -> 7 or 8
    "Pendiente escrituracion",  # 7
    "Escritura",  # 8
    "Pendiente AC aprobación de maqueta",  # 9 -> 11
    "Promesa modificada",  # 10 -> PROMESA_MODIFICADA_STATE
    "Pendiente JP aprobación de maqueta",  # 11 -> 1
    "Pendiente aprobación de firma comprador",  # 12 -> 2
    "Pendiente revisión negociación",  # 13 -> 14     send condition to JP review
    "Pendiente negociación inmobiliaria",  # 14 -> 15 or 1
    "Rechazada Inmobiliaria",  # 15
    "Desistimiento",  # 16 -> PROMESA_DESISTIMIENTO_STATE + PROMESA_REFUND_STATE
    "Resciliación",  # 17 -> PROMESA_RESCILIACION_STATE + PROMESA_REFUND_STATE
    "Resolución",  # 18 -> PROMESA_RESOLUCION_STATE + PROMESA_REFUND_STATE
    "Modificación",  # 19 -> PROMESA_MODIFICACION_STATE + PROMESA_REFUND_STATE
    "Envío a cliente", #20 -> 12
]

PROMESA_DESISTIMIENTO_STATE = [
    "Pendiente aprobación",
]

PROMESA_RESCILIACION_STATE = [
    "Pendiente JP aprobación",
    "Pendiente GC aprobación",
    "Pendiente IN aprobación",
    "Pendiente confección de resciliación",
    "Pendiente firma de resciliación",
]

PROMESA_RESOLUCION_STATE = [
    "Pendiente JP aprobación",
    "Pendiente GC aprobación",
    "Pendiente IN aprobación",
    "Pendiente confección de resolución",
]

PROMESA_MODIFICACION_STATE = [
    "Pendiente JP aprobación",
]

PROMESA_REFUND_STATE = [
    "Pendiente devolución garantía",
    "Refund"
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
    FINANZA = "Finanza"
    MARKETING = "Marketing"


FILE_NON_EXISTED = 'no_existed'
