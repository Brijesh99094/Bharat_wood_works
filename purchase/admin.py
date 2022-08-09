from django.contrib import admin
from .models import *

# Register your models here.
class warehouse(admin.ModelAdmin):
    list_display = ('id','warehouse_name','area')
    search_fields = ('warehouse_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Warehouse, warehouse)

class stock(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'product','qty')
    search_fields = ('warehouse', 'product')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Stock, stock)

class product(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'size','unit','hole_size','holes','is_active')
    search_fields = ('product_name','size','unit')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Product, product)


class purchase(admin.ModelAdmin):
    list_display = ('id','purchase_date','warehouse','supplier','truck_owner','truck_no','weight')
    search_fields = ('warehouse','supplier')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Purchase, purchase)



class purchasereturn(admin.ModelAdmin):
    list_display = ('id','purchase_return_date','warehouse','supplier','truck_owner','truck_no','weight')
    search_fields = ('warehouse','supplier')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(PurchaseReturn,purchasereturn)


class purchase_return_has_product(admin.ModelAdmin):
    list_display = ('id','purchase_return', 'product','qty')
    search_fields = ('product','qty')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Purchase_Return_has_Product,purchase_return_has_product)


class purchase_has_product(admin.ModelAdmin):
    list_display = ('id','purchase', 'product','qty','price')
    search_fields =  ('product','qty','price')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Purchase_has_Product,purchase_has_product)

class supplier(admin.ModelAdmin):
    list_display = ('id','supplier_name', 'mobile','address','is_active')
    search_fields =  ('supplier_name','mobile')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Supplier,supplier)

class transportation(admin.ModelAdmin):
    list_display = ('id','co_name', 'mobile','area','is_active')
    search_fields =  ('co_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Transportation,transportation)


class supervisor_has_warehouse(admin.ModelAdmin):
    list_display = ('id', 'supervisor', 'warehouse')
    search_fields = ('supervisor','warehouse',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(SupervisorHasWarehouse,supervisor_has_warehouse)

class supervisor_has_company(admin.ModelAdmin):
    list_display = ('id', 'supervisor', 'company')
    search_fields = ('supervisor','company',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(SupervisorHasCompany,supervisor_has_company)











