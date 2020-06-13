# Generated by Django 3.0.5 on 2020-06-02 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0008_auto_20200602_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название кафедры'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название факультета'),
        ),
        migrations.AlterField(
            model_name='specialty',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название специальности'),
        ),
    ]