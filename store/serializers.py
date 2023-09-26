from decimal import Decimal
from rest_framework import serializers
from store.models import Products,Collections,Review,Cart,CartItem,Customers,Order,OrderItems

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




#Cart take cartItems from CartItem serializers (parent - cart , child - cartItem):----------------------------

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ['pk', 'title','unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() 
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem 
        fields = ['id','product_id','quantity'] #those field get from DB . if need extra data in varibale then we use self.request -> get data from url through get_context(self.kwagrs['paramsName-which get from urls/users']) for serializer.

    #data validation which get from url/users: if user input wrong product_id then => 
    def validate_product_id(self,value):
        if not Products.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Product Fount with the given ID')
        return value
    
    def save(self, **kwargs): #*** in serializer can't get params from urls , that's why use get_context() method in views to pass data into serializer.
        #in views we are using => serializer.is_validate():  -> serializer.save() 
        cart_id = self.context['cart_id'] #get from  views.context(method)
        product_id = self.validated_data['product_id'] #get from  urls
        quantity = self.validated_data['quantity'] #get from  urls

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)  #if get cart item then just update cartItem. and increase the quantity.
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item#if Model get any data then update and return instance
        except CartItem.DoesNotExist:
            product = Products.objects.get(pk=product_id)
            self.instance = CartItem.objects.create(cart_id=cart_id, product=product, quantity=quantity)#if not found any cartItem then create new Item
             #  or user => 
             #  self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance #if model not get any data then create new instance then return to db.


class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta : 
        model = CartItem 
        fields = ['quantity']

        




class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True )  # Set read_only=True
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()]) #most important Line.

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']



# ----------------------------------Customer Serializer-------------------------------------------------------

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta: 
        model = Customers
        fields = ['id', 'user_id', 'phone', 'email', 'birth_date', 'membership']








# ----------------------------------OrderItem Serializer-------------------------------------------------------

# class OrderItemSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer()

#     class Meta: 
#         model = OrderItems
#         fields = ['id', 'product', 'unit_price', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta: 
        model = OrderItems
        fields = ['id', 'product', 'unit_price', 'quantity']



# ----------------------------------Order Serializer-------------------------------------------------------

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','payment_status', 'customers', 'place_order','items' ]


# ----------------------------------------Create OrderSerializer--------------------------------------------
from django.db import transaction
from .singnals import order_created #

class CreateOrderSerializer(serializers.Serializer):
     #we are not uing the model serializer here...

       #for real life senerio for creating order , we collect data from cart . that's why we use cart_id varibale here .
    cart_id = serializers.UUIDField()#for creating the order we collect cart_ID ,

    
    #if cart_id does not exit then user can't create the order: 
   
    
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists() and Cart.objects.filter(pk=cart_id).count()==0 :
            raise serializers.ValidationError('Cart ID not found!')
        elif CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError('Cart is Empty!')
        return cart_id
  

    def save(self,**kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']#get from user form...
            user_id = self.context.get('user_id')#get from views.
            customer, created = Customers.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customers=customer)


            #for creating the order items : --------------------------------------------------------
        
            #create a cart_id then create a cart_items: then create OrderItems.
            #using CartItem model for filter card_id from cart table.(then we get the product )
            cart_items = CartItem.objects.filter(cart_id=cart_id).select_related('product')

            order_items = [
                OrderItems(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                )
                for item in cart_items
            ]

            OrderItems.objects.bulk_create(order_items)

            #now delete the cartItem cz we use it for creating OrderItems: 

         

            #created singnal fn instance: 
            order_created.send_robust(self.__class__, order = order) #when created the order signal generated.
            
            # Corrected deletion of cart items
            # CartItem.objects.filter(cart_id=cart_id).delete()
            return order #return to the views-> create()

            #we using the model operations=>  order,OrderItem,CartItem, then delete the cartItem ,so if 1 operations 
            #fail then other operations working not properly .... if 1 operation is not work then otherOperations 
            #will stop. that's why we use Tracsictions ORM methods.






# -----------------------------------Udpdate serializers----------------------------------

class UpdateOrderSerializer(serializers.ModelSerializer):
    #just only update the payment_status
    class Meta: 
        model = Order 
        fields = ['payment_status']



