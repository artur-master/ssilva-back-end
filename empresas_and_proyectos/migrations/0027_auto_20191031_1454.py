# Generated by Django 2.1.2 on 2019-10-31 07:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('empresas_and_proyectos', '0026_auto_20191031_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdocument',
            name='CreateAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 31, 7, 54, 49, 307398, tzinfo=utc)),
        ),
    ]
