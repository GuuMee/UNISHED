# Generated by Django 3.0.5 on 2020-06-07 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0026_auto_20200607_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='lector',
            name='disciplines',
            field=models.ManyToManyField(to='univer_structure.Discipline'),
        ),
    ]