# Generated by Django 4.2.3 on 2023-10-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]
