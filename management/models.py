from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    license_no=models.CharField(max_length=200)
    address=models.CharField(max_length=500)
    contact_no=models.CharField(max_length=20)
    email=models.EmailField()
    description=models.CharField(max_length=500,null=True)

    def __str__(self):
        return  self.name



class Medicine(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    batch_no=models.CharField(max_length=200)
    expire_date=models.DateField()
    price_per_item=models.IntegerField()
    prescribe_req=models.BooleanField(default=False)
    mfg_date=models.DateField()
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.name

class Employee(models.Model):

    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    email=models.EmailField(default='pict123@gmail.com')
    prescribed_doc_name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Bill(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)
    amt=models.IntegerField()
    items=models.TextField()

    def __str__(self):
        return self.name

class Orders(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('On the way','On the way'),
        ('delivered','delivered'),
    )
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    medicine=models.ForeignKey(Medicine,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    quantity=models.IntegerField(default=0)
    totalprice=models.IntegerField(default=0)
    peritem=models.IntegerField(default=0)
    status=models.CharField(max_length=200,null=True,choices=STATUS,default="Pending")


    def __str__(self):
        return self.customer.name