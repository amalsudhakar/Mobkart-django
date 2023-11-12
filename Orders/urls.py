from django.urls import path
from . import views


urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('payment', views.payment, name='payment'),
    path('validate_coupon', views.validate_coupon, name='validate_coupon'),
    path('order_completed/<str:order_number>/', views.order_completed, name='order_completed'),
    path('order_failed', views.order_failed, name='order_failed'),
]
