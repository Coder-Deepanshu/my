# Generated by Django 4.2 on 2025-04-26 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0005_b_a_b_com_b_sc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_percent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Student_rollno', models.CharField(max_length=20, unique=True)),
                ('percentage', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
