from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=10, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category
    
@receiver(pre_save, sender=Category)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.category)

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    brand = models.CharField(max_length=50)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category_name.slug, self.slug])

    def __str__(self):
        return self.product_name
    

class VariationCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_name = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.variation_name
    
    def set_is_delete(self, is_deleted):
        self.is_delete = is_deleted
        self.save()
        if is_deleted:
            Variation.objects.filter(variation_category=self).update(is_delete=True)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.ForeignKey(VariationCategory, on_delete=models.CASCADE)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)  # Add a stock field

    def __str__(self):
        return self.variation_value


@receiver(pre_save, sender=Product)
def generated_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.product_name)

    # def __str__(self):
    #     return self.product_name
    
class Image(models.Model):
    name_product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='related_image')
    image = models.ImageField(upload_to='photos/product')

    def __str__(self):
        return f"Image for {self.name_product.product_name}"