# Generated by Django 4.2 on 2025-07-27 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0044_student_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.CharField(default='M', max_length=50),
        ),
    ]
