# Generated by Django 4.2 on 2024-04-17 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IBGECategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField()),
                ('category_name', models.CharField(max_length=100)),
                ('unity', models.CharField(max_length=50)),
                ('level', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IBGEResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ibge_id', models.CharField(max_length=2)),
                ('research_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IBGETerritorialLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territorial_id', models.CharField(max_length=10)),
                ('territorial_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IBGEVariables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var_id', models.IntegerField()),
                ('variable_name', models.CharField(max_length=250)),
                ('unity', models.CharField(max_length=50)),
                ('summarization', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IBGEClassifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classifc_id', models.IntegerField()),
                ('classifc_name', models.CharField(max_length=50)),
                ('status', models.BooleanField()),
                ('exceptions', models.CharField(max_length=100)),
                ('category', models.ManyToManyField(to='dataExtraction.ibgecategories')),
            ],
        ),
        migrations.CreateModel(
            name='IBGEChildAttached',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aggregate_id', models.IntegerField()),
                ('aggregate_name', models.CharField(max_length=700)),
                ('url', models.CharField(max_length=255, null=True)),
                ('subject', models.CharField(max_length=255, null=True)),
                ('frequency', models.CharField(choices=[('P1', 'Anual'), ('P8', 'Semestral'), ('P9', 'Trimestral'), ('P5', 'Mensal'), ('P13', 'Trimestral móvel')], max_length=5, null=True)),
                ('start_freq', models.PositiveIntegerField(null=True)),
                ('end_freq', models.PositiveIntegerField(null=True)),
                ('classifications', models.ManyToManyField(to='dataExtraction.ibgeclassifications')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_aggregated', to='dataExtraction.ibgeresearch')),
                ('territorial_level', models.ManyToManyField(to='dataExtraction.ibgeterritoriallevel')),
                ('variables', models.ManyToManyField(to='dataExtraction.ibgevariables')),
            ],
        ),
    ]
