
from rest_framework.response import Response #serializers to Json formater
from store.models import Products,Collections,OrderItems,Review,Cart,CartItem,Customers
from store.serializers import ProductSerializer,CollectionsSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer
from django.db.models import Count



from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend# filter easyly with any Db.coloumn like price ...
from rest_framework.filters import SearchFilter,OrderingFilter # for search,sorting -> product 
from rest_framework.pagination import PageNumberPagination #paginations
from .filters import ProductFilter 
from store.paginations import DefaultPagination #cutom paginations.

#import for cart:
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .permissions import IsAdminOrReadOnly

class ProductViewSet(ModelViewSet):

    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    #for filter: =>-------------------------
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination  #custom paginations
    # filterset_fields = ['collections_id']
    filterset_class = ProductFilter #import form custom file.
    search_fields  = ['title', 'describtion'] #search box working with those fields.
    ordering_fields = ['unit_price','last_update']
    permission_classes = [IsAdminOrReadOnly]



    def get_serializer_context(self): #for serializer extra variable /mehtod to send to serializer
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
          if OrderItems.objects.filter(product__id=kwargs['pk']).count() > 0:  #aggregations-> count(), ORM query fn-> Count().
                return Response({"error": "product can't be delete cause in orderitem"},)
         
          return super().destroy(request, *args, **kwargs)
  




# --------------------------------collections-------------------------------------



class CollectionViewSet(ModelViewSet):
        permission_classes = [IsAdminOrReadOnly]
        
        queryset = Collections.objects.annotate(products_count=Count('products')).all()
        serializer_class = CollectionsSerializer
        

        def destroy(self, request, *args, **kwargs):
             if OrderItems.products.filter(product__id=kwargs['pk']).count() > 0:  # Changed 'collection' to 'collection'
                return Response({'error': "collections can't be deleted because order items are included"})
             
             return super().destroy(request, *args, **kwargs)
       

class ReviewViewSet(ModelViewSet):
     #cutom query : cz reviews show for every product : filter review for indivisual products.
     def get_queryset(self):
         return Review.objects.filter(product_id =self.kwargs['product_pk'])
     

     #use this method for => send data to Review serializer
     def get_context_data(self) :
         return {'product_id':self.kwargs['product_pk']}
     
     
     serializer_class = ReviewSerializer


class CartViewSet(CreateModelMixin,RetrieveModelMixin,ListModelMixin,DestroyModelMixin,GenericViewSet):
     
    #  queryset = Cart.objects.all()
     queryset = Cart.objects.prefetch_related('items__product').all() #cart -> Fk-> CartItem(related_name=items), instide cartItem Fk-> Products(product) | optimize the query
     serializer_class = CartSerializer


#show single items of cart: 
class CartItemViewSet(ModelViewSet): #tabels need , cart_id, product_id, quantity in DB.
   
    #allow http method : 
    http_method_names = ['get', 'post','patch','delete'] #declare those methods which we want to use.

    #for add cartItem use custom serializer: 
    def get_serializer_class(self):
         if self.request.method == "POST":
              return AddCartItemSerializer #use for add new cartItem.
         elif self.request.method == "PATCH":
              return UpdateCartItemSerializer
         
         return CartItemSerializer # use for get() cartItem.
    

    def get_serializer_context(self): #data collect from urls , then send to serializer 
         return {'cart_id':self.kwargs['cart_pk']}
   


     #need single cartItem hast cart_id column , so need cart_ID+ to catch  :
    def get_queryset(self):
          return CartItem.objects.\
                        filter(cart_id=self.kwargs['cart_pk']).\
                        select_related('product')



#------------------------------Customer user -> JESON WEB TOKEN-------------------------------------------

from rest_framework.decorators import action #get, put, delete ...details = retrive...
from rest_framework.permissions import IsAuthenticated,AllowAny,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly#permisson for users
from .permissions import FullDjangoModelPermission,ViewCustomerModelPermission #cutom permission.

class CustomerViewSet(ModelViewSet):
     queryset = Customers.objects.all()
     serializer_class = CustomerSerializer
     permission_classes = [DjangoModelPermissionsOrAnonReadOnly] #use our custom class : FullDjangoModelPermission.


     @action(detail=True, permission_classes=[ViewCustomerModelPermission]) #custom model permission
     def history(self,request,pk):#http://127.0.0.1:8000/store/customer/1/history....
          return Response('ok')
     
     @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated()])
     def me(self, request):#http://127.0.0.1:8000/store/customer/me/ -> this /me = def me(function). & request.user -> anonimus functions of classes.
          customer, created = Customers.objects.get_or_create(user_id=request.user.id) #get_or_create -> method return 2 value: cutomerID, created/not_created boolean

          if request.method == 'GET':#also show the user id , but user_id can't edit by user. that's why make the CustomerSerializer -> user_id(read_only)
               serializer = CustomerSerializer(customer)
               return Response(serializer.data)

          elif request.method == 'PUT':
               serializer = CustomerSerializer(customer, data=request.data)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               return Response(serializer.data)

     

