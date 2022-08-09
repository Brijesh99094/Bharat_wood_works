from django.db import models
from django.core.validators import RegexValidator
from inventory.models import * 
# Create your models here.

class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=30)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.warehouse_name


 
class Product(models.Model):
    product_name = models.CharField(max_length=40)
    size     = models.CharField(max_length=30)
    unit     = models.CharField(max_length=30,null=True)
    holes    = models.CharField(max_length=20,default=" ")
    hole_size= models.CharField(max_length=20,default=" ")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name+' '+ self.size + self.unit+' '+self.holes


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    qty     = models.IntegerField(null=False,blank=True)

    def __str__(self):
        return self.product.product_name

class Supplier(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    supplier_name = models.CharField(max_length=40,blank=True)
    mobile     = models.CharField(max_length=13,blank=True)
    address     = models.TextField(max_length=70)    
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    gst_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric]) 
    is_active       = models.BooleanField(default=True)

    def __str__(self):
        return self.supplier_name

class Transportation(models.Model):
    co_name = models.CharField(max_length=30,null=True)
    mobile     = models.CharField(max_length=13,blank=True)
    address     = models.TextField(max_length=120,null=True,blank=False) 
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    is_active       = models.BooleanField(default=True)
    def __str__(self):
        return self.co_name


class Purchase(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]', 'Only alphanumeric characters are allowed.')
    purchase_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
    supplier = models.ForeignKey(Supplier,on_delete=models.DO_NOTHING)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    truck_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    weight   = models.CharField(max_length=30,null=True)

    def __str__(self):
        return str(self.id)
     

class Purchase_has_Product(models.Model):
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True,blank=False)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True,blank=False)
    qty     = models.IntegerField(null=True,blank=False)
    price   = models.IntegerField(null=True,blank=False)
   
class PurchaseReturn(models.Model):
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,null=True,blank=False)
    purchase_return_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    supplier = models.ForeignKey(Supplier,on_delete=models.DO_NOTHING,null=True)
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]', 'Only alphanumeric characters are allowed.')
    truck_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    weight   = models.CharField(max_length=30,null=True)

    def __str__(self):
        return str(self.id)

class Purchase_Return_has_Product(models.Model):
    purchase_return = models.ForeignKey(PurchaseReturn,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    qty     = models.IntegerField(null=False,blank=True)
    price   = models.IntegerField(null=True,blank=False)


class SupervisorHasWarehouse(models.Model):
    supervisor = models.ForeignKey(Supervisor,on_delete=models.DO_NOTHING,null=True,blank=False)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING,null=True,blank=False)

class SupervisorHasCompany(models.Model):
    supervisor = models.ForeignKey(Supervisor,on_delete=models.DO_NOTHING,null=True,blank=False)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=True,blank=False)















