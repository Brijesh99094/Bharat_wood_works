from django.db import models
from purchase.models import *
from django.core.validators import RegexValidator
from inventory.models import *
# Create your models here.





class Sales(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]', 'Only alphanumeric characters are allowed.')
    sales_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    lr_no = models.IntegerField(null=False,blank=True,default=0)
    truck_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    weight   = models.CharField(max_length=30,null=True)
    sales_user = models.ForeignKey(Customer,on_delete=models.DO_NOTHING, blank=False, null=True)
    def __str__(self):
        return str(self.id)

class Sales_has_product(models.Model):
    sales = models.ForeignKey(Sales,on_delete=models.CASCADE,null=True,blank=False)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True,blank=False)
    qty     = models.IntegerField(null=True,blank=False)
    price  = models.IntegerField(default=0,blank=False)



class SalesReturn(models.Model):
    sales_return_date = models.DateField()
    sales = models.ForeignKey(Sales,on_delete=models.CASCADE,null=True,blank=False)
    warehouse = models.ForeignKey(Warehouse,on_delete=models.DO_NOTHING)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]', 'Only alphanumeric characters are allowed.')
    truck_no = models.CharField(max_length=50, blank=False, null=True, validators=[alphanumeric])
    weight   = models.CharField(max_length=30,null=True)
    sales_user = models.ForeignKey(Account,on_delete=models.DO_NOTHING, blank=False, null=True)
    


    def __str__(self):
        return str(self.id)



class SalesReturn_has_product(models.Model):
    sales_return = models.ForeignKey(SalesReturn,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    qty     = models.IntegerField(null=False,blank=True)
    price   = models.IntegerField(default=0, blank=True)
