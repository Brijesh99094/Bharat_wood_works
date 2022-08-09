from django import forms
from .models import *
from inventory.models import Account, Area

warehouses = Warehouse.objects.filter(is_active = True)
customer =  Customer.objects.all()
dealer = Dealer.objects.all()
truck_owners = Transportation.objects.all()
areas = Area.objects.all()
plants = Plant.objects.all() 
products = Product.objects.all()


d = {
    'class':'custom-select'

}

class PlantForm(forms.ModelForm):
    plant_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    area = forms.ModelChoiceField(queryset=areas,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Plant
        fields = ('plant_name','area','company')

class Warehouse_To_Plant_Form(forms.ModelForm):
    date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs=d))
    plant = forms.ModelChoiceField(queryset=plants,widget=forms.Select(attrs=d))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    expense = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Warehouse_To_Plant
        fields = ('date','warehouse','plant','truck_owner','truck_no','weight','expense')


class Warehouse_To_Plant_Detail_Form(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    qty = forms.IntegerField(widget = forms.NumberInput(attrs= {'class':'form-control','type':'number','min':'1'}))
    class Meta():
        model = Warehouse_To_Plant_Detail
        fields = ('warehouse_to_plant','product','qty')

class Dispatch_Form(forms.ModelForm):
    date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    customer = forms.ModelChoiceField(queryset=customer,widget=forms.Select(attrs={'class':'custom-select'}))
    dealer = forms.ModelChoiceField(queryset=dealer,widget=forms.Select(attrs={'class':'custom-select'}))
    plant = forms.ModelChoiceField(queryset=plants,widget=forms.Select(attrs=d))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    expense = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Dispatch
        fields = ('date','plant','truck_owner','truck_no','weight','expense','customer','dealer')

class DispatchDetail_Form(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    qty = forms.IntegerField(widget = forms.NumberInput(attrs= {'class':'form-control','type':'number','min':'1'}))
    class Meta():
        model = DispatchDetail
        fields = ('dispatch','product','qty')


class Collection_Form(forms.ModelForm):
    date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    customer = forms.ModelChoiceField(queryset=customer,widget=forms.Select(attrs={'class':'custom-select'}))
    dealer = forms.ModelChoiceField(queryset=dealer,widget=forms.Select(attrs={'class':'custom-select'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs=d))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    expense = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Collection
        fields = ('date','warehouse','truck_owner','truck_no','weight','expense','customer','dealer','dispatch')


class CollectionDetail_Form(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    qty = forms.IntegerField(widget = forms.NumberInput(attrs= {'class':'form-control','type':'number','min':'1'}))
    class Meta():
        model = CollectionDetail
        fields = ('collection','product','qty')

class plant_StockForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    plant = forms.ModelChoiceField(queryset=plants,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = plant_Stock
        fields = ('product','plant','qty')
