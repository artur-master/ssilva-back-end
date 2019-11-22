import os
import pytz
from datetime import datetime

# Funcion para nombrar los archivos pdf de una bitacora

def filename_proyecto_detail(instance, filename):
    path = "proyectoDetail"
    ext = filename.split('.')[-1]
    date_str = str(instance.Date)
    date_str = date_str[:19]

    date_to_formated = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    timezone = pytz.timezone('America/Santiago')
    local_date = pytz.utc.localize(date_to_formated).astimezone(timezone)
    date_formated = local_date.strftime("%d-%m-%Y %H-%M-%S")

    format = "Detalle_" + str(instance.ProyectoID.Name) + \
        "_" + str(date_formated) + "." + ext

    return os.path.join(path, format)
