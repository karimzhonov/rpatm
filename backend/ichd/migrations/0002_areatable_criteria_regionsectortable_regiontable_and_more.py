# Generated by Django 4.1.5 on 2023-01-06 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ichd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('delta_order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Criteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('main', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(blank=True, max_length=6, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
            ],
        ),
        migrations.CreateModel(
            name='RegionSectorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('delta_order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegionTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('delta_order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SectorTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True)),
                ('delta_order', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Uploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='xlsx')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='area',
            options={'verbose_name': 'Area', 'verbose_name_plural': 'Areas'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Region', 'verbose_name_plural': 'Regions'},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'verbose_name': 'Sector', 'verbose_name_plural': 'Sectors'},
        ),
        migrations.CreateModel(
            name='SectorTableCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('delta', models.FloatField(blank=True, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.sectortable')),
            ],
        ),
        migrations.AddField(
            model_name='sectortable',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads'),
        ),
        migrations.AddField(
            model_name='sectortable',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.sector'),
        ),
        migrations.CreateModel(
            name='RegionTableCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('delta', models.FloatField(blank=True, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.regiontable')),
            ],
        ),
        migrations.AddField(
            model_name='regiontable',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads'),
        ),
        migrations.AddField(
            model_name='regiontable',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.region'),
        ),
        migrations.CreateModel(
            name='RegionSectorTableCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('delta', models.FloatField(blank=True, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.regionsectortable')),
            ],
        ),
        migrations.AddField(
            model_name='regionsectortable',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads'),
        ),
        migrations.AddField(
            model_name='regionsectortable',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.region'),
        ),
        migrations.AddField(
            model_name='regionsectortable',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.sector'),
        ),
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('index_delta', models.FloatField(blank=True, null=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.area')),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.region')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.sector')),
            ],
        ),
        migrations.CreateModel(
            name='AreaTableCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('delta', models.FloatField(blank=True, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.areatable')),
            ],
        ),
        migrations.AddField(
            model_name='areatable',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.area'),
        ),
        migrations.AddField(
            model_name='areatable',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads'),
        ),
        migrations.AddField(
            model_name='areatable',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.region'),
        ),
        migrations.AddField(
            model_name='areatable',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.sector'),
        ),
    ]
