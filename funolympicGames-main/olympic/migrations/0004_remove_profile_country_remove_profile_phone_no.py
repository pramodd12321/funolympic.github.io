# Generated by Django 4.0.5 on 2022-09-19 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olympic', '0003_profile_country_profile_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_no',
        ),
    ]
