from django.db import models    
from django.core.validators import RegexValidator
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,email,username,password):
        if not email:
            raise ValueError("User must have Email")
        if not username:
            raise ValueError("User must have username")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            #state=state,
            #city=city,
            #address=address,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            username = username
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class Account(AbstractBaseUser,PermissionsMixin):
    username        = models.CharField(max_length=30)
    email           = models.EmailField(verbose_name="email",max_length=60,unique=True)
    date_joined     = models.DateTimeField(verbose_name="date_joined",auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last_login",auto_now=True)
    is_active       = models.BooleanField(default=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)         #------- #
    is_superuser    = models.BooleanField(default=False)
    role            = models.CharField(max_length=10)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return str(self.email)


    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
    


class State(models.Model):
    state_name = models.CharField(max_length=20)
    def __str__(self):
        return self.state_name

class City(models.Model):
    city_name = models.CharField(max_length=20)
    state = models.ForeignKey(State,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.city_name

class Area(models.Model):
    area_name = models.CharField(max_length=20)
    city = models.ForeignKey(City,on_delete=models.DO_NOTHING,null=True,blank=False)
    def __str__(self):
        return self.area_name


class Company(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    company_name = models.CharField(max_length=50)
    account = models.ForeignKey(Account,on_delete=models.DO_NOTHING)
    gst_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    address = models.TextField(max_length=40,null=False,blank=True)
    phone      = models.CharField(max_length=13,blank=False,null=True)
    date_joined = models.DateTimeField(verbose_name="date_joined",null=True,blank=False)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    def __str__(self):
        return self.company_name
    
class Customer(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    customer_name = models.CharField(max_length=20)
    phone      = models.CharField(max_length=13,blank=False,null=True)
    address = models.TextField(max_length=120,blank=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True, validators=[alphanumeric])
    account = models.ForeignKey(Account,on_delete=models.DO_NOTHING,null=True,blank=False)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=True,blank=False)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    def __str__(self):
        return self.customer_name

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=20)
    contact_person = models.CharField(max_length=30,null=True,blank=False)
    phone      = models.CharField(max_length=13,blank=False,null=True)
    address = models.TextField(max_length=40,blank=True)
    account = models.ForeignKey(Account,on_delete=models.DO_NOTHING,null=True,blank=False)
    company = models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=True,blank=False)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    def __str__(self):
        return self.dealer_name

class Supervisor(models.Model):
    supervisor_name = models.CharField(max_length=20)
    date_joined = models.DateTimeField(verbose_name="date_joined",null=True,blank=False)
    phone      = models.CharField(max_length=13,blank=False,null=True)
    account = models.ForeignKey(Account,on_delete=models.DO_NOTHING,null=True,blank=False)
    area = models.ForeignKey(Area,on_delete=models.DO_NOTHING,null=True,blank=False)
    address = models.TextField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.supervisor_name


