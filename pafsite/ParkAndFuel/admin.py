from django.contrib import admin
from django import forms
from ParkAndFuel.models import Customer, Vehicle, Account, FuelType, Address, Phone, MemberType, PaymentKind, Payment, FuelDispense, TankFill, Vehicle


""" 
Customer & Account Section 
"""

class AccountInline(admin.TabularInline):
    # form = VehicleForm
    model = Account
    extra = 0

class PhoneInline(admin.TabularInline):
    # form = VehicleForm
    model = Phone
    extra = 0

class AddressInline(admin.TabularInline):
    # form = VehicleForm
    model = Address
    extra = 0

class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
       ('Basic Information',   {'fields': ['first_name', 'last_name']}),
       ('Login Credentials (not yet used, but good to collect)',   {'fields': ['email', 'password']}),
       ('Date Joined', {'fields': ['date_joined']})
     ]
    inlines = [AccountInline, PhoneInline, AddressInline]


admin.site.register(Customer, CustomerAdmin)

"""
Account & Vehicle Section
"""

class VehInline(admin.TabularInline):
    model = Vehicle
    extra = 0

class AccountAdmin(admin.ModelAdmin):
    fields =  ( 'customer', 'balance', 'service_fee_remain', 'member_type')
    list_display = ( 'customer', 'balance', 'service_fee_remain', 'member_type')
    readonly_fields = ['customer']
    inlines = [VehInline]


admin.site.register(Account, AccountAdmin)

"""
Tanks
"""
admin.site.register(FuelType)

class TankFillAdmin(admin.ModelAdmin):
    # fields =  ( 'fill_date', 'balance', 'service_fee_remain', 'member_type')
    # list_display = ( 'customer', 'balance', 'service_fee_remain', 'member_type')
    readonly_fields = ['amount_remain']

    
    def save_model(self, request, obj, form, change):
        obj.amount_remain = obj.amount_added
        obj.save()

admin.site.register(TankFill, TankFillAdmin)

""" 
Dispense Fuel
"""
admin.site.register(FuelDispense)
# Again, need way to caluclate Drived Price after filling in other information - so adding
# another button and some JS AJAX ? and making it non-editable, etc.

""" 
Member Type Section
"""
class MemberTypeAdmin(admin.ModelAdmin):
    fields = ( 'name', 'monthly_fee')
    list_display = ( 'name', 'monthly_fee')
       
    
admin.site.register(MemberType, MemberTypeAdmin)

"""
Payment Admin Section
"""
class PaymentKindAdmin(admin.ModelAdmin):
    fields = ( 'name', ('flat_charge','percent_charge'))
    list_display = ('name', 'flat_charge', 'percent_charge')

    
admin.site.register(PaymentKind, PaymentKindAdmin)


admin.site.register(Payment)
# Need way to caluclate derived_fee after filling in other information - so adding
# another button and some JS AJAX ?

