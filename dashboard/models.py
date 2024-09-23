from django.db import models
# from members.models import Buyer

class Review(models.Model):
    restaurant = models.ForeignKey('members.Restaurant', on_delete=models.CASCADE)
    buyer = models.ForeignKey('members.Buyer', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_message = models.TextField()

    def __str__(self):
        return f"Review by {self.buyer} for {self.restaurant}"

class CartItem(models.Model):
    user = models.ForeignKey('members.Buyer', on_delete=models.CASCADE)
    food_item = models.ForeignKey('members.FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.food_item.price

class Cart(models.Model):
    user = models.OneToOneField('members.Buyer', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def get_total(self):
        return sum(item.get_total_price() for item in self.items.all())

    def add_item(self, food_item, quantity):
        cart_item, created = CartItem.objects.get_or_create(
            user=self.user,
            food_item=food_item,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        if not self.items.filter(id=cart_item.id).exists():
            self.items.add(cart_item)
 
class OrderItem(models.Model):
    food_item = models.ForeignKey('members.FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_total_price(self):
        return self.quantity * self.price
    
class Order(models.Model):
    restaurant = models.ForeignKey('members.Restaurant', on_delete=models.CASCADE)
    buyer = models.ForeignKey('members.Buyer', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    order_items = models.ManyToManyField(OrderItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Order {self.id} by {self.buyer} at {self.restaurant}"

    def calculate_total_amount(self):
        total_amount = sum(item.get_total_price() for item in self.order_items.all())
        self.total_amount = total_amount
        self.save()
        return total_amount

