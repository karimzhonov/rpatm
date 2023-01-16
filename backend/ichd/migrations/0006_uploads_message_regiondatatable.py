# Generated by Django 4.1.5 on 2023-01-13 05:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ichd', '0005_alter_area_options_alter_areatable_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploads',
            name='message',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.CreateModel(
            name='RegionDataTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('index_delta', models.FloatField(blank=True, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.criteria')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ichd.uploads')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.region')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ichd.sector')),
            ],
            options={
                'verbose_name': 'Region Data Table',
                'verbose_name_plural': 'Region Data Tables',
            },
        ),
    ]
