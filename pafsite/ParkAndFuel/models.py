import datetime
from django.utils import timezone
from django.db import models
from django.forms import ModelForm


ACTIVE_CHOICE = ((True, 'Acitve'), (False, 'Inactive'))

# /Users/Brad/Sites/parkandfuel/db_setup/source.sql

""""""""""""""
""" Tanks """
""""""""""""""

# Could use a record of when invoice goes out, for those deliquient folks.   
# class MemberCharge(models.Model): # ??
#    account = models.ForeignKey(Account)
#    amount  = models.DecimalField()
#    date    = models.DateTimeField()
    
       
class FuelDispense(models.Model): # This will incur a deduction to the account balance.
    vehicle = models.ForeignKey('Vehicle')
    derived_price = models.DecimalField(decimal_places=2, max_digits=7)
    fill_date = models.DateTimeField()
    volume = models.DecimalField(decimal_places=3, max_digits=7)
    profit = models.DecimalField(decimal_places=2, max_digits=7)


class FuelType(models.Model):
    name   = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

# Remember, to calculate price I sum up all of tank_type with non-0 remain.
# Can someday clear out old 0 remain bits.
class TankFill(models.Model):
    amount_added  = models.DecimalField(decimal_places=3, max_digits=7)
    amount_remain = models.DecimalField(decimal_places=3, max_digits=7)
    fill_date     = models.DateTimeField(default=datetime.datetime.now)
    fill_price    = models.DecimalField(decimal_places=2, max_digits=7)
    fuel_type     = models.ForeignKey(FuelType)

    def __unicode__(self):
        return str(self.fill_date) + ' ' + str(self.amount_added) + ' fuel added at a cost of $' + str(self.fill_price)


""""""""""""""""""""""""""""""""""""""
""" Customer, Accounts and Vehciels """
""""""""""""""""""""""""""""""""""""""
class Address(models.Model):
    ADDRESS_KINDS = (
        ('Work', 'Work'),
        ('Home', 'Home'),
    )
    kind      = models.CharField(max_length=100, choices=ADDRESS_KINDS) # choice work, home, ?
    street    = models.CharField(max_length=100)
    city      = models.CharField(max_length=100)
    state     = models.CharField(max_length=100)
    zip_code  = models.IntegerField() 

    customer           = models.ForeignKey('Customer')


    def __unicode__(self):
        return self.customer.first_name + ' ' + self.customer.last_name + ' at ' + self.kind + ' address: ' + self.street + ' ' + str(self.zip_code)    
    
class Phone(models.Model):
    WORK = 'WK'
    HOME = 'HM'
    MOBILE = 'MB'
    PHONE_KINDS = (
        (WORK, 'Work'),
        (HOME, 'Home'),
        (MOBILE, 'Mobile'),
    )
    kind      = models.CharField(max_length=100, choices=PHONE_KINDS) # choice work, home, ?
    number    = models.CharField(max_length=100)

    customer           = models.ForeignKey('Customer')
    
    
class MemberType(models.Model):
    
    name        = models.CharField(max_length=100)
    monthly_fee = models.DecimalField(decimal_places=2, max_digits=7)

    def __unicode__(self):
        return self.name 

class Customer(models.Model):
    first_name        = models.CharField(max_length=100)
    last_name         = models.CharField(max_length=100)

    email             = models.EmailField(max_length=255)
    password          = models.CharField(max_length=100)
    
    active            = models.BooleanField(choices=ACTIVE_CHOICE)
    
    # billing_address   = models.ForeignKey(Address)
    date_joined       = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Account(models.Model):
    
    balance            = models.DecimalField(decimal_places=2, max_digits=7)
    service_fee_remain = models.DecimalField(decimal_places=2, max_digits=7)
    member_type        = models.OneToOneField(MemberType) # how often vehciles on this account are filled
    
    customer = models.ForeignKey(Customer)
    
    def __unicode__(self):
        return self.customer.first_name + ' ' + self.customer.last_name + ' ' + str(self.balance)



class Vehicle(models.Model):
    make   = models.CharField(max_length=100)
    model  = models.CharField(max_length=100)
    color         = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=100)
    
    location      = models.ForeignKey(Address) # This way, only one place to find it.

    tank_size     = models.DecimalField(decimal_places=2, max_digits=7)
    # periodicity   = models.BooleanField(choices=BOOL_CHOICES,default=True) Taken care of by member type, which is at the account level
    fuel_type     = models.ForeignKey(FuelType)

    account       = models.ForeignKey(Account)
    
    def __unicode__(self):
        return self.owner + '\'s ' + self.make + ' ' + self.model
    

""""""""""""""""""""""""""
""" Money Transactions """
""""""""""""""""""""""""""
""" 
  Write now, just the kind that tops 
  up an account - is there any other? 
"""

class PaymentKind(models.Model): # Type of Payment
    name           = models.CharField(max_length=100)
    flat_charge    = models.DecimalField(decimal_places=4, max_digits=7)
    percent_charge = models.DecimalField(decimal_places=4, max_digits=7)
    
    def __unicode__(self):
        return self.name
    
    
class Payment(models.Model): # This is a payment by the customer.
    account      = models.ForeignKey(Account)
    amount       = models.DecimalField(decimal_places=2, max_digits=7)
    date         = models.DateTimeField()
    kind         = models.ForeignKey(PaymentKind)
    derived_fee  = models.DecimalField(decimal_places=2, max_digits=7) # maybe on save of this one, it is a two step process ... what about slider to adjust fee?
    


