from pyexpat.errors import messages

from django.db.models import F
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.template import RequestContext
from .forms import CreateCustomer
from .filters import MedicineFilter
from .models import *
import  json
from django.http import JsonResponse
import datetime

# Create your views here.
@unauthenticated_user
def loginpage(request):

    if request.method == "POST":
            user_name=request.POST.get('username')
            pass_word=request.POST.get('password')

            user=authenticate(request,username=user_name,password=pass_word)

            print(user_name)
            print(pass_word)

            if user is not None:
                    login(request,user)
                    return redirect('mainpage')#name is given in redirect

            else:
                messages.info(request,"Username or Password is incorrect")
                print("user not correct")


    return render(request,'managemet/loginpage.html')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customergrp'])
def mainpage(request):
    pkid=request.user.customer.id
    order=Orders.objects.filter(customer=request.user.customer).filter(status='On the way')
    info={'name':request.user.username,'custid':pkid,'order':order}
    return render(request,'managemet/mainpage.html',info)


def logoutuser(request):
    logout(request)
    return redirect('loginpage')

@unauthenticated_user
def registerpage(request):

    if request.method=="POST":
        name=request.POST.get('Name')
        phone=request.POST.get('Phone')
        address=request.POST.get('Address')
        email=request.POST.get('Email')
        username=request.POST.get('Username')
        password1=request.POST.get('Password')
        password2=request.POST.get('Password2')

        print(password1)
        print(password2)

        if password2==password1:
            user = User.objects.create_user(username, email,password1)
            customer=Customer(user=user,name=name,phone=phone,address=address,email=email)
            user.save()
            customer.save()
            grp = Group.objects.get(name='customergrp')
            user.groups.add(grp)

            return redirect('loginpage')

        else:
            print('password do not match')




    return render(request,'managemet/registerpage.html')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customergrp'])
def orderpage(request):

    medicines=Medicine.objects.all()

    print(medicines)

    myfilter=MedicineFilter(request.GET,queryset=medicines)
    medicines=myfilter.qs

    context={'myfilter':myfilter,'med':medicines}
    return render(request,'managemet/orderpage.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customergrp'])
def viewprofile(request):
    custid=request.user.customer.id
    customerprof=Customer.objects.get(id=custid)

    form=CreateCustomer(instance=customerprof)

    formlist={'form' : form}

    if request.method=="POST":
       form=CreateCustomer(request.POST,instance=customerprof)

       if form.is_valid():
            form.save()
            return redirect('mainpage')


    return render(request,'managemet/viewprofile.html',formlist)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customergrp'])
def viewpreviousorders(request):
    allorders=request.user.customer.orders_set.all()
    listinfo={'allorders':allorders}
    return render(request,'managemet/viewpreviousorders.html',listinfo)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customergrp'])
def billpage(request):


    return render(request,'managemet/bill.html')

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def dashboard(request):
    current_date = datetime.date.today()
    print(current_date)
    order=Orders.objects.filter(date_created__startswith=current_date).filter(status='Pending')

    context={'order':order}
    print(order)
    return render(request,'managemet/dashboard.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def viewcustomer(request):
    customers=Customer.objects.all()

    context={'customers':customers}

    return render(request,'managemet/viewcustomer.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def viewcustprofile(request,pk):
    customer=Customer.objects.get(id=pk)
    context={'name':customer.name,'phone':customer.phone,'email':customer.email,'address':customer.address,'id':pk}

    return render(request,'managemet/viewcustprofile.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def viewcompany(request):
    companies=Company.objects.all()
    context={'companies':companies}

    return render(request,'managemet/viewcompany.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def viewonecompany(request,pk):
    company=Company.objects.get(id=pk)
    context={'company':company}

    return render(request,'managemet/viewonecompany.html',context)

@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['owner'])
def viewmedicines(request):
    medicines=Medicine.objects.all()
    context={'medicines':medicines}

    return  render(request,'managemet/viewmedicines.html',context)

def deletecustomer(request,pk):
    context = {}

    customer = Customer.objects.get(id=pk)

    context["name"] = customer.name

    if request.method == "POST":
        customer.delete()
        return redirect('dashboard')

    return render(request, 'managemet/deletecustomer.html', context)


def deletecompany(request,pk):
    context = {}

    customer = Company.objects.get(id=pk)

    context["name"] = customer.name

    if request.method == "POST":
        customer.delete()
        return redirect('dashboard')

    return render(request, 'managemet/deletecustomer.html', context)

def vieworderofcust(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.orders_set.all()



    context={'order':orders}


    return render(request,'managemet/vieworderofcust.html',context)



def addItem(request):
    data=json.loads(request.body)
    customer=request.user.customer;
    medicine=Medicine.objects.get(name=data['name'])
    print(customer)
    print(medicine)
    order=Orders.objects.create(customer=customer,medicine=medicine,quantity=int(data['quantity']),totalprice=int(data['total']),peritem=int(data['price']))
    order.save()
    Medicine.objects.filter(name=data['name']).update(quantity=F('quantity')-data['quantity'])
    print(data['name'])
    print(data['price'])
    print(data['quantity'])
    print(data['total'])

    return JsonResponse('item was added',safe=False)

def orderstock(request,pk):
    Medicine.objects.filter(id=pk).update(quantity=F('quantity') +1)
    print("in orderstock")
    medicines = Medicine.objects.all()
    context = {'medicines': medicines}
    return render(request, 'managemet/viewmedicines.html', context)


def updateStatus(request,pk):
    Orders.objects.filter(id=pk).update(status="On the way")

    current_date = datetime.date.today()
    print(current_date)
    order = Orders.objects.filter(date_created__startswith=current_date).filter(status='Pending')

    context = {'order': order}
    print(order)
    return render(request, 'managemet/dashboard.html', context)


def orderReceived(request,pk):
    Orders.objects.filter(id=pk).update(status="delivered")

    pkid = request.user.customer.id

    order = Orders.objects.filter(id=pkid).filter(status='On the way')
    info = {'name': request.user.username, 'custid': pkid, 'order': order}

    return  render(request,'managemet/mainpage.html',info)



