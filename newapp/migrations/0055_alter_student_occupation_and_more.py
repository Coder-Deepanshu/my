# Generated by Django 4.2 on 2025-07-31 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0054_alter_student_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='occupation',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='other_phone_no',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
