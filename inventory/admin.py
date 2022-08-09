from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
class Useradmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff', 'role')
    search_fields = ('email', 'username')
    readonly_fields = ('last_login', 'date_joined')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, Useradmin)


class state(admin.ModelAdmin):
    list_display = ('id','state_name')
    search_fields = ('state_name',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(State, state)

class city(admin.ModelAdmin):
    list_display = ('id','city_name','state')
    search_fields = ('city_name','state')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(City, city)

class area(admin.ModelAdmin):
    list_display = ('id','area_name','city')
    search_fields = ('area','city')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Area, area)


class company(admin.ModelAdmin):
    list_display = ('id','company_name', 'account','gst_no','address','phone','date_joined','area')
    search_fields = ('company_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Company, company)


class customer(admin.ModelAdmin):
    list_display = ('id', 'customer_name','area', 'phone', 'gst_no', 'account','company','address')
    search_fields = ('customer_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Customer, customer)


class dealer(admin.ModelAdmin):
    list_display = ('id', 'dealer_name','area', 'phone', 'account','company','contact_person','address')
    search_fields = ('dealer_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Dealer,dealer)

class supervisor(admin.ModelAdmin):
    list_display = ('id', 'supervisor_name','area', 'phone', 'account','date_joined')
    search_fields = ('supervisor_name',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Supervisor,supervisor)
