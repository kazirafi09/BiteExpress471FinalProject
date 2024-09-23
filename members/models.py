from django.db import models
from dashboard.models import Review
from django.core.validators import MinLengthValidator, RegexValidator
class Buyer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=128, validators=[
        MinLengthValidator(8),
        RegexValidator(
            regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must be at least 8 characters long and include letters, numbers, and special characters.'
        )
    ])
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=128, validators=[
        MinLengthValidator(8),
        RegexValidator(
            regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must be at least 8 characters long and include letters, numbers, and special characters.'
        )
    ])
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    def __str__(self):
        return self.name


class Deliveryman(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255)
    password = models.CharField(max_length=128, validators=[
        MinLengthValidator(8),
        RegexValidator(
            regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must be at least 8 characters long and include letters, numbers, and special characters.'
        )
    ])
    vehicle_number = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    