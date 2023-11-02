from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from Store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Accounts.models import AddressBook
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.

def _cart_id(request):
    cart_id = request.session.get("cart_id")
    print("Session Key:", request.session.session_key)
    if cart_id is None:
        # Generate a new cart_id if it's None
        cart_id = request.session.session_key
        request.session["cart_id"] = cart_id
    return cart_id


def get_or_create_cart(user, cart_id):
    try:
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        cart = Cart(cart_id=cart_id)
        cart.save()
    if user.is_authenticated and cart.user is None:
        cart.user = user
        cart.save()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_variations = []

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('variations_'):
                category_name = key.replace('variations_', '')
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__variation_name=category_name,
                        variation_value=value
                    )
                    product_variations.append(variation)
                except Variation.DoesNotExist:
                    pass

    cart_id = _cart_id(request)
    cart = get_or_create_cart(current_user, cart_id)

    matching_cart_item = None

    for cart_item in cart.cartitem_set.all():
        if cart_item.product == product and set(cart_item.variations.all()) == set(product_variations):
            matching_cart_item = cart_item
            break

    if matching_cart_item:
        matching_cart_item.quantity += 1
        matching_cart_item.save()
    else:
        cart_item = CartItem(
            user=current_user if current_user.is_authenticated else None,
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
        cart_item.variations.set(product_variations)

    return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total/100)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    cart_id = request.session.get("cart_id")
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'cart_id': cart_id
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total/100)
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    address = AddressBook.objects.filter(user=request.user) 
    print(request.user)
    print(address)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address': address
    }
    return render(request, 'store/checkout.html', context)


def save_new_address(request):
    if request.method == 'POST':
        # Get the address data from the POST request
        name = request.POST.get('name')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        phone = request.POST.get('phone')

        # Get the current user (make sure you have authentication set up)
        user = request.user

        if not (name and address_line_1 and state and city and pincode and country and phone):
            return JsonResponse({'error': 'Invalid form data'})

        # Create and save a new address
        new_address = AddressBook.objects.create(
            name=name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            state=state,
            city=city,
            pincode=pincode,
            country=country,
            phone=phone,
            user=user,  # Set the user field to the current user
            status=False  # Set the status as needed
        )

        return JsonResponse({
            'id': new_address.id,
            'name': new_address.name,
            'city': new_address.city,
            'state': new_address.state,
            'phone': new_address.phone,
        })

    # Handle invalid form data
    return JsonResponse({'error': 'Invalid form data'})


def add_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')