# Generated by Django 4.2 on 2025-01-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verify', '0003_documenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='AadhaarRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aadhaar_number', models.CharField(max_length=12, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
            ],
        ),
    ]
