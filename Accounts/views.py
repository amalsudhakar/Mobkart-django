from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import Account, AddressBook
from .forms import RegistrationForm, AddressForm
from django.contrib import messages, auth
from functools import wraps
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from Carts.models import Cart, CartItem
from Carts.views import _cart_id
import requests
from Orders.models import Order


def redirect_authenticated_user(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("store")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def register(request):
    if "email" in request.session:
        return redirect("/")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                username=username,
            )
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Registration Success")
            return redirect("register")
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "Accounts/register.html", context)


def login(request):
    if "email" in request.session:
        return redirect("/")
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)
        try:
            user_exist = Account.objects.get(email=email)
        except:
            messages.error(request, "email doesnt exist")
            return redirect("login")
        if user is not None and user.is_admin is False:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            request.session["email"] = user.email
            request.session["uid"] = user.id
            request.session["first_name"] = user.first_name
            request.session["last_name"] = user.last_name
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                print("query -> ", query)
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                return redirect("dashboard")
        else:
            messages.error(request, "invalid login credentials")
            return redirect("login")
    if request.session.get("username"):
        return redirect("store")
    return render(request, "Accounts/login.html")


# Logout view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("login")


# Dashboard of user
@login_required(login_url="login")
def dashboard(request):
    orders = Order.objects.order_by("-created_at").filter(
        user_id=request.user.id, is_ordered=True
    )
    orders_count = orders.count()
    uid = request.session.get("uid")
    user = Account.objects.get(pk=uid)
    context = {
        "orders_count": orders_count,
        "user": user,
    }
    return render(request, "Accounts/dashboard.html", context)


# My orders page in user profile
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.id, is_ordered=True).order_by(
        "-created_at"
    )
    context = {
        "orders": orders,
    }
    return render(request, "orders/my_orders.html", context)


# View address page
def address_book(request):
    current_user = request.user
    address = AddressBook.objects.filter(user=current_user, is_deleted=False)
    context = {
        "address": address,
    }
    return render(request, "Accounts/address_book.html", context)


# Add address form
def add_address(request):
    form = AddressForm()
    context = {
        "form": form,
    }
    return render(request, "Accounts/add_address.html", context)


# Add address
def save_address(request):
    current_user = request.user
    if request.method == "POST":
        print(current_user)
        user = current_user
        name = request.POST["name"]
        address_line_1 = request.POST["address_line_1"]
        address_line_2 = request.POST["address_line_2"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        pincode = request.POST["pincode"]
        phone = request.POST["phone"]
        status = request.POST["status"]
        address = AddressBook(
            user=user,
            name=name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            phone=phone,
            pincode=pincode,
            status=status,
            country=country,
        )
        address.save()
        if status == "True":
            AddressBook.objects.filter(user=user).exclude(pk=address.pk).update(
                status="False"
            )

        return redirect("address_book")

    else:
        return redirect("add_address")


# Activate address
def activate_address(request):
    a_id = str(request.GET["id"])
    AddressBook.objects.update(status=False)
    AddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({"bool": True})


# Delete address
def delete_address(request, aid):
    address = AddressBook.objects.get(id=aid)
    other_addresses = AddressBook.objects.filter(status=False).exclude(id=aid)
    if address.status is True:
        if other_addresses.exists():
            # Update the status of the first other address to True
            up_add = other_addresses.first()
            up_add.status = True
            up_add.save()

    # Delete the specified address
    address.delete()
    return redirect("address_book")
