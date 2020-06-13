# Generated by Django 3.0.5 on 2020-06-07 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0028_auto_20200607_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discipline',
            name='department',
        ),
        migrations.AddField(
            model_name='discipline',
            name='department',
            field=models.ManyToManyField(to='univer_structure.Department'),
        ),
    ]