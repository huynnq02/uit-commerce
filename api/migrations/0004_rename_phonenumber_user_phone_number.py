# Generated by Django 4.2.1 on 2023-06-01 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_phonenumber_user_phonenumber'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
    ]
