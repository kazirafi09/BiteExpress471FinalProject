from django.urls import path
from . import views
urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('restaurant-registration/', views.register_restaurant_user, name='restaurant_registration'),
    path('delivery_registration/', views.delivery_registration, name='delivery_registration'),
    path('login/', views.login_user, name = "login_user"),
    path('forget_password', views.forget_password, name="forget_password")
]