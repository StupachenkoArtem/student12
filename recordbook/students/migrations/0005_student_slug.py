# Generated by Django 4.2.2 on 2023-07-06 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_group_options_alter_student_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='slug',
            field=models.SlugField(max_length=255, null=True, verbose_name='URL'),
        ),
    ]
