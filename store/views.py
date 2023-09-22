from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.decorators import api_view 
from rest_framework import generics
from rest_framework.response import Response #serializers to Json formater
from store.models import Products,Collections
from store.serializers import ProductSerializer,CollectionsSerializer
from django.shortcuts import get_object_or_404 #if object not found then raise error ...
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_204_NO_CONTENT
from django.db.models import Count



@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        products = Products.objects.select_related('collections')
        serializer = ProductSerializer(products, many=True, context={'request': request}) #connected with => name = contact-detiails
        return Response(serializer.data)
    

    elif request.method=='POST': #Create Product----------------------------------------
        serializer = ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True) #if Error => then raise Error massage.
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)



@api_view(['GET', 'PUT','DELETE'])
def product_details(request, sku): #Read/Update/Delete Product----------------------------------------
    product = get_object_or_404(Products, pk=sku)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT': 
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    elif request.method =='DELETE':
        if product.orderItems.count() > 0:  #aggregations-> count(), ORM query fn-> Count().
            return Response({"error": "product can't be delete cause in orderitem"},)
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)



@api_view()
def collection(request,pk):
    return Response('ok')

# --------------------------------collections-------------------------------------




@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        query_set = Collections.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionsSerializer(query_set,many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
    if request.method == "POST":
        serializer = CollectionsSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)




@api_view(['GET','PUT','DELETE'])
def collections_details(request, pk):

    collection = get_object_or_404(
        Collections.objects.annotate(products_count=Count('products')), pk=pk )

    if request.method == 'GET':
        product_count = collection.products_count
        serializer = CollectionsSerializer(collection)
        data = serializer.data
        data['product_count'] = product_count
        return Response(data, status=HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CollectionsSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error':"collections can't be deleted because order items are included"})
        collection.delete()
        return Response(status=HTTP_204_NO_CONTENT)


