# Generated by Django 5.0 on 2023-12-19 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authuser', '0007_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default_avatar.jpg', null=True, upload_to='avatars/'),
        ),
    ]