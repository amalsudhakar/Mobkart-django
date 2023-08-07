# Generated by Django 4.2.3 on 2023-07-22 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_remove_category_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/product')),
                ('name_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.product')),
            ],
        ),
    ]
