# Generated by Django 5.1.5 on 2025-01-16 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_session_film'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='ticket_price',
            field=models.IntegerField(default=300),
        ),
    ]
