# Generated by Django 4.2 on 2024-05-04 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataExtraction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ibgechildattached',
            name='territorial_level',
        ),
        migrations.AddField(
            model_name='ibgechildattached',
            name='research',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='IBGETerritorialLevel',
        ),
    ]
