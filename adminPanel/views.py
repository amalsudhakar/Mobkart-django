from django.shortcuts import render, redirect
from django.contrib import messages, auth
from Store.models import Category, Product
from Accounts.models import Account
from .forms import ProductForm


def adminPanel(request):
    if 'email' in request.session:
        return redirect('adminHome')
    else:
        return render(request, 'admin/admin_panel.html')


def adminLogin(request):
    if 'email' in request.session:
        return redirect('adminHome')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_superadmin is True:
                auth.login(request, user)
                # categories = Category.objects.all()
                # context = {
                #     'categories': categories
                # }
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                request.session['is_admin'] = True
                return redirect('adminHome')
            else:
                messages.error(request, 'not an admin')
                return redirect('adminPanel')
    return render(request, 'admin/admin_panel.html')


def adminHome(request):
    return render(request, 'admin/admin_home.html')


def adminLogout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('adminLogin')


def product_details(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = request.POST['product_name']
            description = request.POST['description']
            price = request.POST['price']
            brand = request.POST['brand']
            stock = request.POST['stock']
            is_available = request.POST['is_available']
            category_id = request.POST['category_name']
            category = Category.objects.get(pk=category_id)

            product = Product(
                product_name=product_name,
                description=description,
                price=price,
                brand=brand,
                stock=stock,
                is_available=is_available,
                category_name=category
            )
            product.save()

            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'admin/admin_home.html', {'form': form, 'categories': categories})


def add_product(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admin/add_product.html', context)


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/product_list.html', context)


def product_disable(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/disable_product.html', context)


def disable_product(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(pk=product_id)
    product.is_delete = True
    product.save()
    return redirect(product_disable)

def enable_product(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(pk=product_id)
    product.is_delete = False
    product.save()
    return redirect(product_disable)


def userList(request):
    users = Account.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'admin/user_list.html', context)


def blockUser(request):
    user_id = request.POST.get('user_id')
    user = Account.objects.get(pk=user_id)
    user.is_blocked = True
    user.save()
    return redirect(blockedUser)


def unBlockUser(request):
    user_id = request.POST.get('user_id')
    user = Account.objects.get(pk=user_id)
    user.is_blocked = False
    user.save()
    return redirect(userList)


def blockedUser(request):
    users = Account.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'admin/blocked_users.html', context)