# Generated by Django 3.0.5 on 2020-06-09 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0031_auto_20200609_2228'),
        ('schedule', '0012_auto_20200609_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disciplinelessons',
            name='discipline',
        ),
        migrations.AddField(
            model_name='disciplinelessons',
            name='discipline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplinelessons', to='univer_structure.Discipline'),
        ),
    ]
