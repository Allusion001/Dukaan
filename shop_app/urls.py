from django.urls import path
from . import views

urlpatterns=[
    path('products',views.products,name="products"),
    path('product_detail/<slug:slug>',views.product_detail,name="products_details"),
    path('add_item/',views.add_item,name="add_to_cart"),
    path('product_in_cart',views.product_in_cart,name="product_in_cart"),
    path('get_cart',views.get_cart,name="get_cart"),
    path('get_cart_stat',views.get_cart_stat,name="get_cart_stat"),
    path('update_quantity/',views.update_quantity,name="update_quantity"),
    path('delete_cartitem/',views.delete_cartitem,name="delete_carttime"),
    path('get_username/',views.get_username,name="get_username"),
    path('user_info',views.user_items,name="get_user_items"),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_failed', views.payment_failed, name='payment_failed')


]