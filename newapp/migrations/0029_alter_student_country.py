# Generated by Django 4.2 on 2025-07-20 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0028_student_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='country',
            field=models.CharField(max_length=50),
        ),
    ]
