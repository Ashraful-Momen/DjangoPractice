from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework.response import Response #serializers to Json formater
from store.models import Products,Collections,OrderItems,Review
from store.serializers import ProductSerializer,CollectionsSerializer,ReviewSerializer
from django.shortcuts import get_object_or_404 #if object not found then raise error ...
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_204_NO_CONTENT
from django.db.models import Count
from rest_framework.views import APIView



from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet



class ProductViewSet(ModelViewSet):
    queryset = Products.objects.select_related('collections')
    serializer_class = ProductSerializer

    def get_serializer_context(self): #for serializer extra variable /
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


