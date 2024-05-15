from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_signup, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('addProduct/', views.add_product, name='addProduct'),
    path('cart/', views.cart, name="cart"),
    path('order_history/', views.order_history, name="order_history"),
    path('main/', views.main, name="main"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('profile/', views.profile, name='profile'),
    path('productHistory/', views.product_history, name='productHistory'),
]