# Generated by Django 3.0.5 on 2020-06-02 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0004_auto_20200602_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
