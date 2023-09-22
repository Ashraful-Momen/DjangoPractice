from django_filters.rest_framework import FilterSet 
from store.models import Products

class ProductFilter(FilterSet):

    class Meta: 

        model = Products 
        
        fields = {
            'collections_id': ['exact'],
            'unit_price' : ['gt','lt']
        }
