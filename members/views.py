import random
from django.shortcuts import render, redirect
from .models import FoodItem, Buyer, Restaurant, Deliveryman
from .forms import  BuyerRegisterForm, RestaurantRegisterForm, DeliveryManRegisterForm, ForgetPasswordForm
from django.contrib import messages

def register_user(request):
    if request.method == "POST":
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('register_user')
        else:
            messages.error(request, 'Registration failed. Please correct the errors in the form. Thank You.')
    else:
        form = BuyerRegisterForm()

    cities = {
        'Dhaka': 'members/dhaka.jpg',
        'Chittagong': 'members/chittagon.jpg',
        'Bagerhat': 'members/bagerhat.jpg',
        'Bandarban': 'members/bandarban.jpeg',
        'Barguna': 'members/barguna.webp',
        'Barishal': 'members/barishal.jpg',
        'Chadpur': 'members/chadpur.jpeg',
        'Bogra': 'members/bogra.jpg',
        'Brahmanbaria': 'members/brahmanbaria.jpg',
    }
    
    context = {
        'form': form,
        'cities': cities
    }
    return render(request, 'members/landing.html', context)

def register_restaurant_user(request):
    if request.method == "POST":
        form = RestaurantRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_user')
    else:
        form = RestaurantRegisterForm()
    return render(request, 'members/restaurant_reg.html' , {"form":form})

def delivery_registration(request):
    if request.method == "POST":
        form = DeliveryManRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_user')
    else:
        form = DeliveryManRegisterForm()
    return render(request, 'members/deliveryman_reg.html' , {"form":form})

def authenticate_user(email, password):
    try:
        buyer = Buyer.objects.get(email=email)
        if buyer.password == password:
            return buyer, 'Buyer'
    except Buyer.DoesNotExist:
        pass
    try:
        restaurant = Restaurant.objects.get(email=email)
        if restaurant.password == password:
            return restaurant, 'Restaurant'
    except Restaurant.DoesNotExist:
        pass  
    try:
        deliveryman = Deliveryman.objects.get(email=email)
        if deliveryman.password == password:
            return deliveryman, 'Deliveryman'
    except Deliveryman.DoesNotExist:
        pass 
    return None, None

def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user, user_type = authenticate_user(email, password)
        if user is not None:
            request.session['user_type'] = user_type
            request.session['user_email'] = user.email
            request.session['user_name'] = user.name
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('register_user')
    
    return render(request, 'members/landing.html')

def forget_password(request):
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = None
            for model in [Buyer, Restaurant, Deliveryman]:
                if model.objects.filter(email=email).exists():
                    user = model.objects.get(email=email)
                    break
            if user:
                user.password = new_password
                user.save()
                return redirect('register_user')
    else:
        form = ForgetPasswordForm()

    return render(request, 'members/forget_password.html', {'form': form})