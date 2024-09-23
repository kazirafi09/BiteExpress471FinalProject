from django import forms
from members.models import FoodItem

class AddFooditemsForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'price', 'description']

class RestaurantSearchForm(forms.Form):
    restaurant_name = forms.CharField(label='Restaurant Name', max_length=100)
    
class AddToCartForm(forms.Form):
    food_item_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=1)

    