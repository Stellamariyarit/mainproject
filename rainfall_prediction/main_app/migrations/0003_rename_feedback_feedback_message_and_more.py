# Generated by Django 5.1.6 on 2025-02-26 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_feedback_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feedback',
            new_name='message',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='user',
        ),
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]
