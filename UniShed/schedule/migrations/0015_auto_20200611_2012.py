# Generated by Django 3.0.5 on 2020-06-11 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0032_auto_20200610_1857'),
        ('schedule', '0014_auto_20200610_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplinelessons',
            name='lector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessonlectors', to='univer_structure.Lector'),
        ),
        migrations.DeleteModel(
            name='LectorAttachedDiscipline',
        ),
    ]
