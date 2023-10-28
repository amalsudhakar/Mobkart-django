from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from Store.models import (
    Category,
    Product,
    Variation,
    VariationCategory,
    ProductCategoryConnection,
)
from Accounts.models import Account
from .forms import ProductForm
from django.views.decorators.http import require_POST
from django.db.models import Q

def adminPanel(request):
    if "email" in request.session:
        return redirect("adminHome")
    else:
        return render(request, "admin/admin_panel.html")


def adminLogin(request):
    if "email" in request.session:
        return redirect("adminHome")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_superadmin is True:
                auth.login(request, user)
                # categories = Category.objects.all()
                # context = {
                #     'categories': categories
                # }
                request.session["user_id"] = user.id
                request.session["email"] = user.email
                request.session["is_admin"] = True
                return redirect("adminHome")
            else:
                messages.error(request, "not an admin")
                return redirect("adminPanel")
    return render(request, "admin/admin_panel.html")


def adminHome(request):
    return render(request, "admin/admin_home.html")


def adminLogout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("adminLogin")


def product_details(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = request.POST["product_name"]
            description = request.POST["description"]
            price = request.POST["price"]
            brand = request.POST["brand"]
            stock = request.POST["stock"]
            is_available = request.POST["is_available"]
            category_id = request.POST["category_name"]
            category = Category.objects.get(pk=category_id)

            product = Product(
                product_name=product_name,
                description=description,
                price=price,
                brand=brand,
                stock=stock,
                is_available=is_available,
                category_name=category,
            )
            product.save()

            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request, "admin/admin_home.html", {"form": form, "categories": categories}
    )


def add_product(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "admin/add_product.html", context)


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "admin/product_list.html", context)


def product_disable(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "admin/disable_product.html", context)


def disable_product(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(pk=product_id)
    product.is_delete = True
    product.save()
    return redirect(product_disable)


def enable_product(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(pk=product_id)
    product.is_delete = False
    product.save()
    return redirect(product_disable)


def userList(request):
    users = Account.objects.all()
    context = {"users": users}
    return render(request, "admin/user_list.html", context)


def blockUser(request):
    user_id = request.POST.get("user_id")
    user = Account.objects.get(pk=user_id)
    user.is_blocked = True
    user.save()
    return redirect(blockedUser)


def unBlockUser(request):
    user_id = request.POST.get("user_id")
    user = Account.objects.get(pk=user_id)
    user.is_blocked = False
    user.save()
    return redirect(userList)


def blockedUser(request):
    users = Account.objects.all()
    context = {"users": users}
    return render(request, "admin/blocked_users.html", context)


def delete_view_variation(request):
    variations = Variation.objects.all()
    context = {
        "variations": variations,
    }
    return render(request, "admin/view_variation.html", context)


def disable_variation(request):
    variation_id = request.POST.get("variation_id")
    variations = Variation.objects.get(id=variation_id)
    variations.is_delete = True
    variations.save()
    return redirect("delete_view_variation")


def enable_variation(request):
    variation_id = request.POST.get("variation_id")
    variations = Variation.objects.get(id=variation_id)
    variations.is_delete = False
    variations.save()
    return redirect("delete_view_variation")


def add_variation(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }
    return render(request, "admin/add_variation.html", context)


def save_variation(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        variation_category = request.POST.get("variation_category", "").strip()

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return redirect("error_view")

        existing_category = VariationCategory.objects.filter(
            category=category, variation_name__iexact=variation_category).first()

        if existing_category:
            messages.error(
                request,
                f"The category '{variation_category}' already exists for this product.",
            )
            return redirect("add_variation")

        new_variation = VariationCategory(
            category=category, variation_name=variation_category
        )
        new_variation.save()

        products_with_category = Product.objects.filter(category_name=category)

        for product in products_with_category:
            (
                product_connection,
                created,
            ) = ProductCategoryConnection.objects.get_or_create(product=product)
            product_connection.categories.add(new_variation)

        return redirect("view_variation_category")


def add_variant(request):
    variations = VariationCategory.objects.all()
    products = ProductCategoryConnection.objects.all()
    context = {
        "variations": variations,
        "products": products,
    }
    print(products)
    print(variations)
    return render(request, "admin/add_varient.html", context)


def save_varient(request):
    if request.method == "POST":
        variation_value = request.POST.get("variant").strip()
        variation_id = request.POST.get("variation")
        product_id = request.POST.get("product_name")
        try:
            variation = VariationCategory.objects.get(id=variation_id)
        except VariationCategory.DoesNotExist:
            return redirect("error_view")

        product = Product.objects.get(id=product_id)

        # Check if a variation with the same name already exists for the given product and variation category
        existing_variation = Variation.objects.filter(
            Q(variation_value__iexact=variation_value),
            product=product,
            variation_category=variation
        ).first()

        if existing_variation:
            messages.error(request, f"Variant '{variation_value}' already exists for this product.")
            return redirect("add_variant")
        else:
            # Create a new variation
            variation_instance, created = Variation.objects.get_or_create(
                product=product,
                variation_category=variation,
                variation_value=variation_value,
            )

            variation_instance.is_active = True
            variation_instance.is_delete = False
            variation_instance.stock = 0
            variation_instance.save()

            return redirect("view_variation_category")

    return redirect("error_view")


def view_variation_category(request):
    variations = VariationCategory.objects.all()
    context = {
        "variations": variations,
    }
    return render(request, "admin/view_variation_category.html", context)


def updateview_variation(request):
    products = Product.objects.filter(is_delete=False)
    product_connections = ProductCategoryConnection.objects.filter(product__in=products)

    variations = Variation.objects.all()

    context = {
        "products": products,
        "variations": variations,
        "product_connections": product_connections,
    }

    return render(request, "admin/update_stock.html", context)


@require_POST
def update_stock(request):
    product_id = request.POST.get("product_id")
    stock_amount = request.POST.get("stock_amount")
    selected_category_values = []

    for key, value in request.POST.items():
        if key.startswith("selected_category_values_"):
            selected_category_values.append(value)

    try:
        product = Product.objects.get(id=product_id)

        # Update the stock for each selected variation
        for variation_id in selected_category_values:
            variation = Variation.objects.get(id=variation_id)
            variation.stock += int(stock_amount)
            variation.save()
        product.stock += int(stock_amount)
        product.save()
        return redirect("delete_view_variation")

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"})

    except Variation.DoesNotExist:
        return JsonResponse({"error": "Variation not found"})


def updateview_nonvarient(request):
    products_not_in_connection = Product.objects.exclude(productcategoryconnection__isnull=False)
    
    context = {
        'products_not_in_connection': products_not_in_connection,
    }
    
    return render(request, "admin/update_nonvarient_stock.html", context)


def update_stock_non_variant(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('stock')

        try:
            product = Product.objects.get(id=product_id)
            product.stock = new_stock
            product.save()
            return JsonResponse({'success': True, 'new_stock': new_stock, 'product_id': product_id})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    
    # If there's a validation error or an invalid request, return an appropriate JSON response.
    return JsonResponse({'success': False, 'message': 'Validation error or invalid request'}, status=400)