# Generated by Django 5.0 on 2023-12-21 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_gamestats'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamehistory',
            options={'verbose_name': 'Game History', 'verbose_name_plural': 'Game History'},
        ),
        migrations.AlterModelOptions(
            name='gameroom',
            options={'verbose_name': 'Game Room', 'verbose_name_plural': 'Game Rooms'},
        ),
        migrations.AlterModelOptions(
            name='gamestats',
            options={'verbose_name': 'Game Stats', 'verbose_name_plural': 'Game Stats'},
        ),
    ]