# Generated by Django 4.2.13 on 2024-12-10 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='descryption',
            new_name='description',
        ),
    ]