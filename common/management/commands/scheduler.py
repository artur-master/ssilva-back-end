import requests
import datetime

from django.core.management.base import BaseCommand, CommandError

from apscheduler.schedulers.blocking import BlockingScheduler

from time import strftime


from common import constants

from common.models import UF
from common.models import APIUpdate

from common.services import get_or_none

sched = BlockingScheduler()

# @sched.scheduled_job('interval', hours=2)

# CronJob para poblar modelo de uf desde api mindicador
# Falta dejar ejecutado el servicio continuamente en el servidor
# Comando para ejecutar cronjob python manage.py scheduler

@sched.scheduled_job('cron', day_of_week='wed', hour=11, minute=22) 
def poblar_uf_hasta_fecha_valida():
    date = datetime.datetime.now()
    now = date.date()
    api_update = APIUpdate.objects.get(Name="UF")

    uf = get_or_none(UF, Date=now)
    
    if not uf:
        i = 1
        for i in range(0, 31+1):
            next_day = date + datetime.timedelta(days=i)
            next_day = next_day.date().strftime("%d-%m-%Y")
            data = constants.API_UF_URL + next_day
            request = requests.get(data, headers={"User-Agent":"Mozilla/5.0"})
            ufs = request.json()
            if ufs['serie']:
                for uf in ufs['serie']:
                    date = uf['fecha'][0:10]
                    UF.objects.create(
                        Date=date,
                        Value=uf['valor'],
                    )
            else:
                break
        api_update.Date = now
        api_update.save()


def poblar_uf_year(year):
    data = constants.API_UF_URL + str(year)
    request = requests.get(data, headers={"User-Agent": "Mozilla/5.0"})
    ufs = request.json()

    for uf in ufs['serie']:
        date = uf['fecha'][0:10]
        UF.objects.create(
            Date=date,
            Value=uf['valor']
        )


class Command(BaseCommand):
    help = 'Poblar modelo UF en un determinado tiempo'

    def handle(self, *args, **options):
        sched.start()


