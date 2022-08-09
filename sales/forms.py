from .models import *
from django import forms


warehouses = Warehouse.objects.filter(is_active=True)
sales_users = Customer.objects.filter()
truck_owners = Transportation.objects.all()
area = Area.objects.all()
products = Product.objects.all()


class SalesForm(forms.ModelForm):
    sales_date = forms.CharField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    warehouse = forms.ModelChoiceField(
        queryset=warehouses, widget=forms.Select(attrs={'class': 'custom-select'}))
    sales_user = forms.ModelChoiceField(
        queryset=sales_users, widget=forms.Select(attrs={'class': 'custom-select'}))
    truck_owner = forms.ModelChoiceField(
        queryset=truck_owners, widget=forms.Select(attrs={'class': 'custom-select'}))
    truck_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text'}))
    weight = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text'}))

    class Meta():
        model = Sales
        fields = ('sales_date', 'warehouse', 'truck_owner',
                  'truck_no', 'weight', 'sales_user')


class SalesProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=products, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta():
        model = Sales_has_product
        fields = ('sales', 'product', 'qty', 'price')


class SalesReturnForm(forms.ModelForm):
    class Meta():
        model = SalesReturn
        fields = ('sales_return_date', 'warehouse', 'truck_owner',
                  'truck_no', 'weight', 'sales_user')


class SalesReturnProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=products, widget=forms.Select(attrs={'class': 'custom-select'}))

    class Meta():
        model = SalesReturn_has_product
        fields = ('sales_return', 'product', 'qty', 'price')
