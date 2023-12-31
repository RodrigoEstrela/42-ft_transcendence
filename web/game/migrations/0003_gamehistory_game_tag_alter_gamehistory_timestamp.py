# Generated by Django 5.0 on 2023-12-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_gamehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamehistory',
            name='game_tag',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='gamehistory',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, unique_for_date=True),
        ),
    ]
