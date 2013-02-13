from django.contrib import admin
from django import forms
from ParkAndFuel.models import Customer, Vehicle, Account, TankSet, Address, Phone, MemberTypes, PaymentKind, Payment, FuelDispense, TankFill, Vehicle


# class VehicleForm( forms.ModelForm ):
   # query   = forms.CharField( widget=forms.Textarea( attrs={'style': 'font-family: courier' } ) )
   # name    = forms.CharField( widget=forms.Textarea )
    # this removes the 'name' in the tbl.  hmm, weird.  errCode = forms.CharField( widget=forms.TextInput(attrs={'size':'20'}) )
  #   class Meta:
    #    model = Vehicle
        #exclude = ['date_added','date_updated','order'] # no good as along as I don't have default values for these guys

class VehicleInline(admin.TabularInline):
    # form = VehicleForm
    model = Vehicle
    extra = 0

class AccountInline(admin.TabularInline):
    # form = VehicleForm
    model = Account
    extra = 0
    inlines = [VehicleInline]

class PhoneInline(admin.TabularInline):
    # form = VehicleForm
    model = Phone
    extra = 0

class AddressInline(admin.TabularInline):
    # form = VehicleForm
    model = Address
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    # fieldsets = [
     #   ('Customer',   {'fields': ['first_name']}),
    # ]
    inlines = [AccountInline, PhoneInline, AddressInline]

admin.site.register(MemberTypes)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Payment)
admin.site.register(PaymentKind)

