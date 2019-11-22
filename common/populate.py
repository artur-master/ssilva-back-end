import requests
import datetime

from time import strftime
from common import constants
from common.models import UF
from common.services import get_or_none

# Funciones para efectuar llamada a la api de las ufs (mindicador.cl/uf)


def poblar_uf_rango(year_from, year_to):
    for i in range(year_from, year_to + 1):
        data = constants.API_UF_URL + str(i)
        request = requests.get(data, headers={"User-Agent": "Mozilla/5.0"})
        ufs = request.json()

        for uf in ufs['serie']:
            # Se obtiene solo fecha dejando fuera la hora
            date = uf['fecha'][0:10]
            UF.objects.create(
                Date=date,
                Value=uf['valor']
            )

# Funcion para guardar las ufs de un año en especifico


def poblar_uf_year(year):
    data = constants.API_UF_URL + str(year)
    request = requests.get(data, headers={"User-Agent": "Mozilla/5.0"})
    ufs = request.json()

    for uf in ufs['serie']:
        # Se obtiene solo fecha dejando fuera la hora
        date = uf['fecha'][0:10]
        UF.objects.create(
            Date=date,
            Value=uf['valor']
        )
