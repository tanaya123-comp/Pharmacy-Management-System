from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('loginpage/',loginpage,name="loginpage"),
    path('mainpage/',mainpage,name="mainpage"),
    path('logoutpage/',logoutuser,name='logoutpage'),
    path('registerpage/',registerpage,name="registerpage"),
    path('orderpage/',orderpage,name='orderpage'),
    path('viewprofile/',viewprofile,name='viewprofile'),
    path('viewpreviousorders/',viewpreviousorders,name='viewpreviousorders'),
    path('bill/',billpage,name="billpage"),
    path('dashboard',dashboard,name="dashboard"),
    path('viewcustomer',viewcustomer,name='viewcustomer'),
    path('viewcustprofile/<str:pk>/',viewcustprofile,name="viewcustprofile"),
    path('viewcompany/',viewcompany,name="viewcompany"),
    path('viewonecompany/<str:pk>/',viewonecompany,name="viewonecompany"),
    path('viewmedicines',viewmedicines,name="viewmedicines"),
    path('addItem/',addItem,name="addItem"),
    path('vieworderofcust/<str:pk>/',vieworderofcust,name="vieworderofcust"),
    path('deletecustomer/<str:pk>/',deletecustomer,name="deletecustomer"),
    path('deletecompany/<str:pk>/', deletecompany, name="deletecompany"),
    path('orderstock/<str:pk>/',orderstock,name="orderstock"),
    path('updatestatus/<str:pk>/',updateStatus,name="updatestatus"),
    path('orderrec/<str:pk>/',orderReceived,name="orderrec")

]