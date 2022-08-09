from django.contrib import admin
from .models import *


class plant(admin.ModelAdmin):
    list_display = ('id','plant_name','company','area')
    search_fields = ('plant_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Plant,plant)

class plant_stock(admin.ModelAdmin):
    list_display = ('id','plant','product','qty')
    search_fields = ('plant',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(plant_Stock,plant_stock)


class Warehouse_To_plant(admin.ModelAdmin):
    list_display = ('id','warehouse','plant','truck_owner','truck_no','weight','expense')
    search_fields = ('warehouse','plant')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Warehouse_To_Plant,Warehouse_To_plant)

class Warehouse_To_Plant_detail(admin.ModelAdmin):
    list_display = ('id','warehouse_to_plant','product','qty')
    search_fields = ('product','qty')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Warehouse_To_Plant_Detail,Warehouse_To_Plant_detail)

class dispatch(admin.ModelAdmin):
    list_display = ('date','customer','plant','truck_owner','truck_no','weight','expense')
    search_fields = ('customer','plant')
admin.site.register(Dispatch,dispatch)

class dispatch_detail(admin.ModelAdmin):
    list_display = ('id','dispatch','product','qty')
    search_fields = ('product','qty')
admin.site.register(DispatchDetail,dispatch_detail)

class collection(admin.ModelAdmin):
    list_display = ('date','customer','warehouse','truck_owner','truck_no','weight','expense')
    search_fields = ('customer','collection')
admin.site.register(Collection,collection)

class collection_detail(admin.ModelAdmin):
    list_display = ('id','collection','product','qty')
    search_fields = ('product','qty')
admin.site.register(CollectionDetail,collection_detail)
