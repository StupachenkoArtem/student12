# Generated by Django 4.2.2 on 2023-06-22 15:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
                ('birth_date', models.DateField(default=datetime.date(2000, 1, 1), verbose_name='Дата Рождения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_study', models.BooleanField(default=True, verbose_name='Учится')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
            ],
        ),
    ]
