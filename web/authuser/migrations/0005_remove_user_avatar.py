# Generated by Django 5.0 on 2023-12-19 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0004_alter_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]
