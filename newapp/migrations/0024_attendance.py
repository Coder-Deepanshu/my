# Generated by Django 4.2 on 2025-07-16 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0023_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('leave', 'On Leave'), ('late', 'Late Arrival')], max_length=10)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.faculty')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('faculty', 'date')},
            },
        ),
    ]
