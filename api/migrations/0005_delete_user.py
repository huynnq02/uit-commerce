# Generated by Django 4.2.1 on 2023-06-02 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_phonenumber_user_phone_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
