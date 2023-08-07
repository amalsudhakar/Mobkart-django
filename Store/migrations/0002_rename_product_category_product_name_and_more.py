# Generated by Django 4.2.3 on 2023-07-22 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='product',
            new_name='product_name',
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=500)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='photos/product')),
                ('brand', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Store.category')),
            ],
        ),
    ]
