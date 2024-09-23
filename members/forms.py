from .models import Buyer, Restaurant, Deliveryman
from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
class BuyerRegisterForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = "__all__"
class RestaurantRegisterForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['rating']
class DeliveryManRegisterForm(forms.ModelForm):
    class Meta:
        model = Deliveryman
        fields = "__all__"

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField()
    new_password = forms.CharField(widget=forms.PasswordInput(), validators=[
        MinLengthValidator(8),
        RegexValidator(
            regex='^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Password must be at least 8 characters long and include letters, numbers, and special characters.'
        )
    ])
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data