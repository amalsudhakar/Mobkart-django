
from django.urls import path
from . import views 

urlpatterns = [
     path('register/', views.register, name='register'),
     path('login/', views.login, name='login'),
     path('logout/', views.logout, name='logout'),
     path('dashboard/', views.dashboard, name='dashboard'),
     path('', views.dashboard, name='dashboard'),
     path('my_orders/', views.my_orders, name='my_orders'),
     path('address_book/', views.address_book, name='address_book'),
     path('add_address/', views.add_address, name='add_address'),
     path('save_address/', views.save_address, name='save_address'),
     path('activate_address', views.activate_address, name='activate_address'),
     path('delete_address/<int:aid>/', views.delete_address, name='delete_address'),

]
