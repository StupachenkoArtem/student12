# Generated by Django 4.2.2 on 2023-07-03 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_group_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.group', verbose_name='Группа'),
        ),
    ]
