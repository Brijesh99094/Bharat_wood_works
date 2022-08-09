from django.contrib import admin
from .models import *

class salesmaster(admin.ModelAdmin):
    list_display = ('id','sales_date','warehouse','truck_owner','truck_no','lr_no','weight','sales_user')
    search_fields = ('warehouse',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Sales, salesmaster)



class sales_has_product(admin.ModelAdmin):
    list_display = ('id','sales', 'product','qty','price')
    search_fields =  ('product','qty')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Sales_has_product,sales_has_product)



class salesreturn(admin.ModelAdmin):
    list_display = ('id','sales_return_date','warehouse','truck_owner','truck_no','weight','sales_user')
    search_fields = ('warehouse',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(SalesReturn,salesreturn)


class sales_return_has_product(admin.ModelAdmin):
    list_display = ('id','sales_return', 'product','qty')
    search_fields = ('product','qty')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(SalesReturn_has_product,sales_return_has_product)






