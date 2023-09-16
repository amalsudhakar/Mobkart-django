# Generated by Django 4.2.3 on 2023-09-11 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_product_is_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varitation_category', models.CharField(choices=[('color', 'color'), ('storage', 'storage')], max_length=50)),
                ('variation_value', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
            ],
        ),
    ]