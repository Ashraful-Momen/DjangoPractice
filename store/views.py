
from rest_framework.response import Response #serializers to Json formater
from store.models import Products,Collections,OrderItems,Review
from store.serializers import ProductSerializer,CollectionsSerializer,ReviewSerializer
from django.db.models import Count



from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend# filter easyly with any Db.coloumn like price ...
from rest_framework.filters import SearchFilter,OrderingFilter # for search,sorting -> product 
from rest_framework.pagination import PageNumberPagination #paginations
from .filters import ProductFilter 
from store.paginations import DefaultPagination #cutom paginations.

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



    def get_serializer_context(self): #for serializer extra variable /mehtod to send to serializer
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
          if OrderItems.objects.filter(product__id=kwargs['pk']).count() > 0:  #aggregations-> count(), ORM query fn-> Count().
                return Response({"error": "product can't be delete cause in orderitem"},)
         
          return super().destroy(request, *args, **kwargs)
  




# --------------------------------collections-------------------------------------



class CollectionViewSet(ModelViewSet):
        
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


