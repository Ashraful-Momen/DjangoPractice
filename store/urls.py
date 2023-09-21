from django.urls import path
from store import views

urlpatterns = [
    path('product_list/',views.product_list,name='product_list' ),
    path('product/<str:sku>/', views.product_details, name='product'),
    path('collections/<int:pk>/', views.collection, name='collection-detials'), # serializer method - 4 . 

]