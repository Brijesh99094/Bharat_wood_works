from django import forms
from django.contrib.auth import authenticate #for login authentication
from inventory.models import *
from purchase.models import *
from django.contrib.auth.forms import UserCreationForm

warehouses   = Warehouse.objects.all()
companys = Company.objects.all()
areas = Area.objects.all()
class Registration(UserCreationForm):
    email           = forms.EmailField(max_length=60,help_text='Entered email address must be valid')
    role            = forms.CharField(max_length=10)

    class Meta:
        model = Account
        fields = ('email','username','password1','password2','role')

class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password')

    class Meta():
        model = Account
        fields = ('email','password')
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        

class CustomerDetailForm(forms.ModelForm): 
    customer_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    area = forms.ModelChoiceField(queryset=areas,widget=forms.Select(attrs={'class':'custom-select'}))
    address = forms.CharField(widget = forms.Textarea(attrs= {'class':'form-control','rows':'3'}))
    gst_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text','pattern':'[0-9,A-Z]{15}'}))
    phone  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}'}))
    company = forms.ModelChoiceField(queryset=companys,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Customer
        fields = ('customer_name','area','phone','gst_no','account','address','company')

        
class DealerDetailForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=areas,widget=forms.Select(attrs={'class':'custom-select'}))
    dealer_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    contact_person = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    address = forms.CharField(widget = forms.Textarea(attrs= {'class':'form-control','rows':'3'}))
    phone  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}'}))
    company = forms.ModelChoiceField(queryset=companys,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = Dealer
        fields = ('dealer_name','contact_person','phone','address','account','company','area')

class SupervisorDetailForm(forms.ModelForm):
    address = forms.CharField(widget = forms.Textarea(attrs= {'class':'form-control','rows':'3'}))
    supervisor_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    phone  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}'}))
    area = forms.ModelChoiceField(queryset=areas,widget=forms.Select(attrs={'class':'custom-select'}))
    date_joined = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    class Meta():
        model = Supervisor
        fields = ('supervisor_name','date_joined','phone','account','address','area')

class CompanyDetailForm(forms.ModelForm):
    area = forms.ModelChoiceField(queryset=areas,widget=forms.Select(attrs={'class':'custom-select'}))
    company_name = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text'}))
    address = forms.CharField(widget = forms.Textarea(attrs= {'class':'form-control','rows':'3'}))
    gst_no = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'text','pattern':'[0-9,A-Z]{15}'}))
    phone  = forms.CharField(widget = forms.TextInput(attrs= {'class':'form-control','type':'tel','pattern':'[0-9]{10}'}))
    date_joined = forms.CharField(widget = forms.DateInput(attrs= {'class':'form-control','type':'date'}))
    class Meta():
        model = Company
        fields = ('company_name','gst_no','date_joined','phone','account','address','area')

class SupervisorHasWarehouseForm(forms.ModelForm):
    warehouse = forms.ModelChoiceField(queryset=warehouses,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = SupervisorHasWarehouse
        fields = ('warehouse','supervisor')

class SupervisorHasCompanyForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=companys,widget=forms.Select(attrs={'class':'custom-select'}))
    class Meta():
        model = SupervisorHasCompany
        fields = ('company','supervisor')

