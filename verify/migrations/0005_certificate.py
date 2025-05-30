# Generated by Django 4.2 on 2025-01-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verify', '0004_aadhaarrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='certificates/')),
                ('extracted_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
