# Generated by Django 4.1.5 on 2023-01-06 12:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ichd', '0002_areatable_criteria_regionsectortable_regiontable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploads',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='uploads',
            name='finish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='uploads',
            name='status',
            field=models.CharField(choices=[('progres', 'In progres'), ('finished', 'Finished')], default='progres', max_length=100),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='sector',
            name='number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
