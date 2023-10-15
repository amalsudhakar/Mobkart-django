from django.shortcuts import render, redirect
from django.http import JsonResponse
from Carts.models import CartItem
from .models import Order, Coupon
from Accounts.models import AddressBook
import datetime
from django.views.decorators.http import require_POST
# Create your views here.


def payments(request):
    return render(request, 'orders/payments.html')



def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total / 100)
    grand_total = total + tax

    if request.method == 'POST':
        # Get the selected address and order note from the form data
        selected_address_id = request.POST.get('selected_address')
        order_note = request.POST.get('order_note')

        try:
            selected_address = AddressBook.objects.get(id=selected_address_id)
        except AddressBook.DoesNotExist:
            selected_address = None

        data = Order()
        data.user = current_user
        data.email = current_user.email
        data.name = selected_address.name if selected_address else ''
        data.address_line_1 = selected_address.address_line_1 if selected_address else ''
        data.address_line_2 = selected_address.address_line_2 if selected_address else ''
        data.country = selected_address.country if selected_address else ''
        data.state = selected_address.state if selected_address else ''
        data.pincode = selected_address.pincode if selected_address else ''
        data.city = selected_address.city if selected_address else ''
        data.phone = selected_address.phone if selected_address else ''
        data.order_note = order_note
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')

        if selected_address:
            # Set the selected address
            data.selected_address = selected_address

        data.save()

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def validate_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    current_total = float(request.POST.get('current_total'))

    # Query the coupon model to check if the coupon exists and get its discount value
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        discount = coupon.amount
    except Coupon.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Invalid coupon code'})

    # Calculate the new total after applying the discount
    new_total = current_total - discount

    # Assuming you have a way to identify the current order, for example, by order ID
    order_id = request.POST.get('order_id')  # Make sure to include the order_id in your AJAX request

    # Update the order total in the Order model
    try:
        order = Order.objects.get(id=order_id)
        order.order_total = new_total
        order.save()
    except Order.DoesNotExist:
        return JsonResponse({'valid': False, 'message': 'Order not found'})

    return JsonResponse({'valid': True, 'new_total': new_total})