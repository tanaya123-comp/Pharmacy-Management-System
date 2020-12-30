import django_filters
from  .models import *

class MedicineFilter(django_filters.FilterSet):
    class Meta:
        model=Medicine
        fields=('name',)