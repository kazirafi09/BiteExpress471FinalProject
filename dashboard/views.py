from django.shortcuts import render, redirect
from members.models import FoodItem, Restaurant, Buyer, Deliveryman
import random
from django.shortcuts import render, get_object_or_404
from members.forms import BuyerRegisterForm, RestaurantRegisterForm, DeliveryManRegisterForm
from django.contrib import messages
from .forms import AddFooditemsForm, RestaurantSearchForm, AddToCartForm
from .models import CartItem, Cart
from .models import Order, OrderItem 
from django.http import JsonResponse 


def dashboard_view(request):
    user_type = request.session.get('user_type')
    user_name = request.session.get('user_name')
    user_email = request.session.get('user_email')
    if user_type == 'Buyer':
        all_restaurants = list(Restaurant.objects.values_list('name', flat=True))
        selected_restaurants = random.sample(all_restaurants, 4) if len(all_restaurants) >= 3 else all_restaurants
        request.session['selected_restaurants'] = selected_restaurants

        restaurant_items = {}
        for restaurant_name in selected_restaurants:
            items = FoodItem.objects.filter(restaurant__name__exact=restaurant_name)[:5]
            restaurant_items[restaurant_name] = items

        if request.method == 'POST':
            form = RestaurantSearchForm(request.POST)
            if form.is_valid():
                search_query = form.cleaned_data['restaurant_name']

                try:
                    restaurant = Restaurant.objects.get(name__iexact=search_query)
                    return redirect('restaurant_menu', user_name=user_name, restaurant_name=restaurant.name)
                except Restaurant.DoesNotExist:
                    matching_items = FoodItem.objects.filter(name__icontains=search_query)
                    restaurant_items = {}
                    for item in matching_items:
                        restaurant_name = item.restaurant.name
                        if restaurant_name not in restaurant_items:
                            restaurant_items[restaurant_name] = []
                        restaurant_items[restaurant_name].append(item)
                    context = {
                        'restaurant_items': restaurant_items,
                        'user_name': user_name,
                        'user_email': user_email,
                        'form': form,
                        'search_query': search_query,
                    }
                    return render(request, 'dashboard/food.html', context)
        else:
            form = RestaurantSearchForm()

        context = {
            'restaurant_items': restaurant_items,
            'user_name': user_name,
            'user_email': user_email,
            'all_restaurants': all_restaurants,
            'form': form,
        }
        return render(request, 'dashboard/buyer_dashboard.html', context)

    elif user_type == 'Restaurant':
        user_type = request.session.get('user_type')
        user_name = request.session.get('user_name')
        user_email = request.session.get('user_email')
        current_restaurant = Restaurant.objects.get(email=user_email)
        all_items = FoodItem.objects.filter(restaurant=current_restaurant)
        form = AddFooditemsForm(request.POST or None)
        
     
        orders = Order.objects.filter(restaurant=current_restaurant).order_by('-created_on')
        
        if request.method == "POST" and form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = current_restaurant
            food_item.save()
            return redirect('dashboard')
        else:
            form = AddFooditemsForm()
            
        context = {
            'user_name': user_name,
            'user_email': user_email,
            'all_items': all_items,
            'description': current_restaurant.description,
            'form': form,
            'orders': orders, 
        }
        return render(request, 'dashboard/restaurant_dashboard.html', context)

    elif user_type == 'Deliveryman':
        user_type = request.session.get('user_type')
        user_name = request.session.get('user_name')
        user_email = request.session.get('user_email')
        context = {
            'user_name' : user_name,
            'user_email' : user_email
        }
        return render(request, 'dashboard/deliveryman_dashboard.html', context)

def restaurant_menu(request, user_name, restaurant_name):
    restaurant = get_object_or_404(Restaurant, name__iexact=restaurant_name)
    menu_items = FoodItem.objects.filter(restaurant=restaurant)
    context = {
        'user_name': user_name,
        'restaurant_name': restaurant_name,
        'menu_items': menu_items,
    }
    return render(request, 'dashboard/restaurant_menu.html', context)

def profile(request):
    user_type = request.session.get('user_type')
    user_email = request.session.get('user_email')
    user = None
    if user_type == 'Buyer':
        user = get_object_or_404(Buyer, email=user_email)
        form_class = BuyerRegisterForm
    elif user_type == 'Restaurant':
        user = get_object_or_404(Restaurant, email=user_email)
        form_class = RestaurantRegisterForm
    elif user_type == 'Deliveryman':
        user = get_object_or_404(Deliveryman, email=user_email)
        form_class = DeliveryManRegisterForm
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.session['user_type'] = user_type
            request.session['user_email'] = user.email
            request.session['user_name'] = user.name
            messages.success(request, "Your profile has been updated.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = form_class(instance=user)
    
    context = {
            'user': user,
            'user_name' : user.name,
            'form':form
    }
    return render(request, 'dashboard/user_profile.html', context)
    


def view_cart(request):
    user = get_object_or_404(Buyer, email=request.session.get('user_email'))
    cart = Cart.objects.filter(user=user).first()

    restaurant_name=None
    if cart and cart.items.exists():
        first_item = cart.items.first()
        if first_item:
           restaurant_name = first_item.food_item.restaurant.name


    if cart is None:
        return render(request, 'dashboard/view-cart.html', {
            'user': None,
            'cart': None,
            'items': [],
            'restaurant_name': None,
    
        })

    context = {
        'user': user,
        'cart': cart,
        'items': cart.items.all() if cart else [],
        'restaurant_name': restaurant_name  
    }
    return render(request, 'dashboard/view-cart.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        food_item_id = request.POST.get('food_item_id')
        quantity = request.POST.get('quantity')

        if food_item_id and quantity:
            try:
                food_item = get_object_or_404(FoodItem, id=food_item_id)
                user = get_object_or_404(Buyer, email=request.session.get('user_email'))

                cart, created = Cart.objects.get_or_create(user=user)
                cart.add_item(food_item, int(quantity))

                return redirect('view-cart')
            except Exception as e:
                print(f"Error adding to cart: {e}")

    return redirect('view-cart')

def remove_from_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        
        if cart_item_id:
            try:
                cart_item = get_object_or_404(CartItem, id=cart_item_id)
                carts = Cart.objects.filter(items=cart_item)
                
                for cart in carts:
                    if cart.items.filter(id=cart_item_id).exists():
                        cart.items.remove(cart_item)
                cart_item.delete()

            except Exception as e:
                print(f"Error removing from cart: {e}")

    return redirect('view-cart')


def get_order_summery(request):
    user = get_object_or_404(Buyer, email=request.session.get('user_email'))
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return JsonResponse({
            'items': [],
            'total': 0
        })

    items = cart.items.all()
    order_details = []

    for item in items:
        order_details.append({
            'food_item': item.food_item.name,
            'quantity': item.quantity,
            'total_price': item.get_total_price()
        })

    return JsonResponse({
        'items': order_details,
        'total': cart.get_total()
    })    


def order_success(request):
    return render(request, 'dashboard/order_success.html')

def place_order(request):
    user = get_object_or_404(Buyer, email=request.session.get('user_email'))

    cart = Cart.objects.filter(user=user).first()

    if cart is None or cart.items.count() == 0:
        return redirect('view-cart')

    first_cart_item = cart.items.first()
    restaurant = first_cart_item.food_item.restaurant

    order = Order.objects.create(
        restaurant=restaurant,
        buyer=user,
        status='PENDING'
    )

    order_items = []
    total_amount = 0
    for cart_item in cart.items.all():
        order_item = OrderItem.objects.create(
            food_item=cart_item.food_item,
            quantity=cart_item.quantity,
            price=cart_item.food_item.price  
        )
        order_items.append(order_item)
        total_amount += order_item.get_total_price()

    order.order_items.set(order_items)

    order.total_amount = total_amount
    order.save()

    cart.items.all().delete()

    return redirect('order_success')

def view_orders(request):
    buyer = get_object_or_404(Buyer, email=request.session.get('user_email'))
    
    orders = Order.objects.filter(buyer=buyer).order_by('-created_on')
    
    return render(request, 'dashboard/orders.html', {'orders': orders})

def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'COMPLETED' 
    order.save()
    return redirect('dashboard')  

