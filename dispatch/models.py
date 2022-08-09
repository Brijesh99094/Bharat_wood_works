from django.db import models
from inventory.models import Company, Area,Customer,Dealer

from purchase.models import Warehouse, Product, Transportation
# Create your models here.


class Plant(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    plant_name = models.CharField(max_length=25)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.plant_name


class plant_Stock(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(null=False, blank=True)

    def __str__(self):
        return self.product.product_name


class Warehouse_To_Plant(models.Model):
    date = models.DateField(null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    truck_no = models.CharField(max_length=50, blank=True, null=True)
    weight   = models.CharField(max_length=30,null=True)
    expense = models.IntegerField(null=True)
    def __str__(self):
        return str(self.id)


class Warehouse_To_Plant_Detail(models.Model):
    warehouse_to_plant = models.ForeignKey(Warehouse_To_Plant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    qty = models.IntegerField(null=False, blank=True)

    def __str__(self):
        return self.product.product_name

class Dispatch(models.Model):
    date = models.DateField(null=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    truck_no = models.CharField(max_length=50, blank=True, null=True)
    weight   = models.CharField(max_length=30,null=True)
    expense = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return str(self.id)

class DispatchDetail(models.Model):
    dispatch = models.ForeignKey(Dispatch,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)

class Collection(models.Model):
    dispatch = models.ForeignKey(Dispatch,on_delete=models.CASCADE,null=True)
    date = models.DateField(null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    truck_owner = models.ForeignKey(Transportation,on_delete=models.DO_NOTHING,null=True)
    truck_no = models.CharField(max_length=50, blank=True, null=True)
    weight   = models.CharField(max_length=30,null=True)
    expense = models.IntegerField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return str(self.id)


class CollectionDetail(models.Model):
    collection = models.ForeignKey(Collection,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(null=True)