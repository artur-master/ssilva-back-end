# Generated by Django 2.1.2 on 2019-03-05 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_rename_ocupation_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='CivilStatusID',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='ContractMarriageTypeID',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='GenreID',
        ),
        migrations.AddField(
            model_name='cliente',
            name='CivilStatus',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='ContractMarriageType',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='Genre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='Nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='CivilStatus',
        ),
        migrations.DeleteModel(
            name='ContractMarriageType',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
    ]
