from itertools import groupby
from django.shortcuts import render, get_object_or_404
from Store.models import Product, Category, Variation
from Carts.models import CartItem
from Carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category_name=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category_name__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()  # noqa: E501


        variations = Variation.objects.filter(product=single_product)
        grouped_variations = {}

        for variation in variations:
            category_name = variation.variation_category.variation_name
            if category_name not in grouped_variations:
                grouped_variations[category_name] = []
            grouped_variations[category_name].append(variation)

        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'grouped_variations': grouped_variations
    }
    return render(request, 'store/product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter( Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
            product_count = products.count()
    context={
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)