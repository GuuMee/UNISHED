# Generated by Django 3.0.5 on 2020-06-03 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univer_structure', '0016_discipline_max_number_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditorium',
            name='type_discipline',
            field=models.CharField(choices=[('Лк. зн.', 'Лекции'), ('Пр. зн.', 'Практика'), ('Лаб. зн.', 'Лабораторные работы')], max_length=10, null=True, verbose_name='Вид учебных занятий'),
        ),
    ]