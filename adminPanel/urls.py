
from django.urls import path
from .import views


urlpatterns = [
   
    path('', views.adminPanel, name="adminPanel"),
    path('adminLogin', views.adminLogin, name="adminLogin"),
    path('adminLogout', views.adminLogout, name="adminLogout"),
    path('adminHome', views.adminHome, name="adminHome"),
    path('add_product', views.add_product, name="add_product"),
    path('product_disable', views.product_disable, name="product_disable"),
    path('disable_product', views.disable_product, name="disable_product"),
    path('enable_product', views.enable_product, name="enable_product"),
    path('product_details', views.product_details, name="product_details"),
    path('product_list', views.product_list, name="product_list"),
    path('user_list', views.userList, name="user_list"),
    path('block_user', views.blockUser, name="block_user"),
    path('blocked_users', views.blockedUser, name="blocked_users"),
    path('unblock_user', views.unBlockUser, name="unblock_user"),
    path('delete_view_variation', views.delete_view_variation, name="delete_view_variation"),
    path('disable_variation', views.disable_variation, name="disable_variation"),
    path('enable_variation', views.enable_variation, name="enable_variation"),
    path('add_variation', views.add_variation, name="add_variation"),
    path('save_variation', views.save_variation, name="save_variation"),
    path('view_variation_category', views.view_variation_category, name="view_variation_category"),
    path('update_stock', views.update_stock, name='update_stock'),
    path('updateview_variation', views.updateview_variation, name='updateview_variation'),
    path('updateview_nonvarient', views.updateview_nonvarient, name='updateview_nonvarient'),
    path('add_varienet', views.add_varienet, name='add_varienet'),
    path('save_varient', views.save_varient, name='save_varient'),
    # path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    
] 
