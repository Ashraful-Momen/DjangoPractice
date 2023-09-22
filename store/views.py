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

    #if use custom query then get error for the base name . parent router should be add the base_name cz query 
    #cz query run according to the basename ...
    
    serializer_class = ProductSerializer

    #for filter product according to collections id , need custom query: 
    def get_queryset(self):
        queryset = Products.objects.all()

        #self.reqeust take value form user;
        #  query_param[] use in url for Sqlquery and return query but it's not work properly, that's why use query.get().
        collection_id = self.request.query_params.get('collection_id') #MultiValueDictKeyError at /store/product : solve the error use query.get()

        if collection_id is not None: 
             queryset = queryset.filter(collections_id=collection_id) #first collections varibale add extra -> s (revers word avoiding)
       
        return queryset


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


