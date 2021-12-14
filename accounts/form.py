from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
    
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

