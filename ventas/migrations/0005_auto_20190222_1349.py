# Generated by Django 2.1.2 on 2019-02-22 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_auto_20190220_1015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ventalog',
            old_name='DocumentScoring',
            new_name='DocumentSimulador',
        ),
    ]
