from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/<str:user_name>/<str:restaurant_name>/', views.restaurant_menu, name='restaurant_menu'),
    path('view-cart/', views.view_cart, name='view-cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('get-order-summery/', views.get_order_summery, name='get_order_summery'),
    path('order-success/', views.order_success, name='order_success'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.view_orders, name='orders'),
    path('complete-order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('dashboard/<str:user_name>/<str:restaurant_name>/', views.restaurant_menu, name='restaurant_menu'),

]

