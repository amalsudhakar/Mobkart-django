# Generated by Django 4.2.3 on 2023-10-16 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
