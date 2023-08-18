import django_filters
from .models import UAV

class UAVFilter(django_filters.FilterSet):
    class Meta:
        model = UAV
        fields = '__all__'