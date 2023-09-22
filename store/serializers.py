from decimal import Decimal
from rest_framework import serializers
from store.models import Products,Collections,Review

class ProductSerializer(serializers.ModelSerializer):
    

    class Meta : 
        model = Products
        fields = ['title', 'price', 'collections','price_with_tax','inventory','describtion'] #first search fields form model , if not find . then search => price , collections, tax_with price

  
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') #custome name price => comes from unit_prime -> product(model)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product:Products):
        return product.unit_price * Decimal(1.1)



class CollectionsSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)  # Add this line

    class Meta: 
        model = Collections
        fields = ['id', 'title', 'products_count']

        


class ReviewSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Review
        fields = ['id', 'date','name', 'describtion','product']

    #Receive data from context method form views.Reveiws (product_id, reviews_also )
    def create(self,validated_data):
        product_id = self.context ['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)

