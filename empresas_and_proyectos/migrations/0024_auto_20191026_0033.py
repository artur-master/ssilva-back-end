# Generated by Django 2.1.2 on 2019-10-25 17:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('empresas_and_proyectos', '0023_auto_20191025_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdocument',
            name='CreateAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 25, 17, 33, 7, 603935, tzinfo=utc)),
        ),
    ]
