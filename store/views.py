from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from store.models import Products
from store.serializers import ProductSerializer
@api_view()
def product_list(request):
    return Response("Ok")

@api_view()
def product(request,id):
    product = Products.objects.get(id)
    serializer = ProductSerializer(product)

    return Response(serializer.data) #dajango autometically convert the data to json formate.


# @api_view()
# def product(request, id):
#     try:
#         product = Products.objects.get(pk=id)  # Use the correct primary key field name
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Products.DoesNotExist:
#         return Response({"error": "Product not found"}, status=404)
