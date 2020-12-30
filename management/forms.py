from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models  import User

class CreateCustomer(ModelForm):
    class Meta:
        model = Customer
        exclude=('user','prescribed_doc_name')

