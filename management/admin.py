from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Medicine)
admin.site.register(Employee)
admin.site.register(Bill)
admin.site.register(Orders)

