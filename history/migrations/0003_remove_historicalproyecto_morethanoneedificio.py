# Generated by Django 2.1.2 on 2019-02-21 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20190220_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproyecto',
            name='MoreThanOneEdificio',
        ),
    ]
