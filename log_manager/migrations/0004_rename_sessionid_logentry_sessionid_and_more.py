# Generated by Django 4.0.4 on 2022-04-20 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_manager', '0003_rename_session_logentry_sessionid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='sessionID',
            new_name='sessionId',
        ),
        migrations.RenameField(
            model_name='logentry',
            old_name='userID',
            new_name='userId',
        ),
    ]
