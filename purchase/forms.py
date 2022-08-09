from .models import *
from django import forms
from django.forms import ModelChoiceField
from .models import SupervisorHasWarehouse


warehouses = Warehouse.objects.filter(is_active = True)
suppliers = Supplier.objects.filter(is_active = True)
truck_owners = Transportation.objects.all()
products = Product.objects.all()
area = Area.objects.all()


d = {
    'class':'custom-select'

}


class StockForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Stock
        fields = ('product','warehouse','qty')

class PurchaseForm(forms.ModelForm):
    purchase_date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs=d))
    supplier = forms.ModelChoiceField(queryset=suppliers,widget=forms.Select(attrs=d))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Purchase
        fields = ('purchase_date','warehouse','supplier','truck_owner','truck_no','weight')
    
    

class PurchaseReturnForm(forms.ModelForm):
    purchase_return_date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs={'class':'custom-select'}))
    supplier = forms.ModelChoiceField(queryset=suppliers,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = PurchaseReturn
        fields = ('purchase_return_date','warehouse','supplier','truck_owner','truck_no','weight')

class PurchaseUpdateForm(forms.ModelForm):
    purchase_date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs={'class':'custom-select'}))
    supplier = forms.ModelChoiceField(queryset=suppliers,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
    truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Purchase
        fields = ('purchase_date','warehouse','supplier','truck_owner','truck_no','weight')


class PurchaseProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Purchase_has_Product
        fields = ('purchase','product','qty','price') # add purchase to see purchase id

class ProductForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = ('product_name','size','unit','hole_size','holes') 

# class PurchaseReturnForm(forms.ModelForm):
#     purchase_return_date = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
#     warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs={'class':'custom-select'}))
#     supplier = forms.ModelChoiceField(queryset=suppliers,widget=forms.Select(attrs={'class':'custom-select'}))
#     truck_owner = forms.ModelChoiceField(queryset=truck_owners,widget=forms.Select(attrs={'class':'custom-select'}))
#     truck_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
#     weight = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
#    class Meta():
#        model = PurchaseReturn
#        fields = ('purchase_return_date','truck_owner',)  

class PurchaseReturnProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=products,widget=forms.Select(attrs={'class':'custom-select'}))
    qty = forms.IntegerField(widget = forms.NumberInput(attrs= {'class':'form-control','type':'number','min':'1'}))
    price = forms.IntegerField(widget = forms.NumberInput(attrs= {'class':'form-control','type':'text'}))
    class Meta():
        model = Purchase_Return_has_Product
        fields = ('purchase_return','product','qty','price') # add purchase to see purchase id

class SupplierForm(forms.ModelForm):
    gst_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text','pattern':'[0-9,A-Z]{15}','title':'Please enter valid GST no'}))
    mobile  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}','title':'Please enter valid Mobile no'}))
    supplier_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    address = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'textarea'}))
    class Meta():
        model = Supplier
        fields = ('supplier_name','mobile','address','gst_no')

class UpdateProductForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = ('product_name','size','unit') 

class WarehouseForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=area,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Warehouse
        fields = ('warehouse_name','area')


class TransportationForm(forms.ModelForm):
    mobile  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}'}))
    co_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    address = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'textarea'}))
    area = forms.ModelChoiceField(queryset=area,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Transportation
        fields = ('co_name','area','address','mobile')