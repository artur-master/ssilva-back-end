# Generated by Django 2.1.2 on 2019-11-08 06:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('empresas_and_proyectos', '0028_auto_20191107_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdocument',
            name='CreateAt',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 8, 6, 15, 37, 582249, tzinfo=utc)),
        ),
    ]
