# Generated by Django 4.0.4 on 2022-04-20 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_manager', '0002_remove_loggedsession_user_logentry_session_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='session',
            new_name='sessionID',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='user',
            new_name='userID',
        ),
    ]
