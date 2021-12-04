from django.forms import ModelForm
from .models import Customer, Order

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'