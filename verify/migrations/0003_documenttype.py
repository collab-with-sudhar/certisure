# Generated by Django 4.2 on 2024-12-31 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verify', '0002_aadhaarusers_dob_panusers_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='documenttype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(max_length=3)),
            ],
        ),
    ]
