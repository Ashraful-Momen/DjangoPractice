from django.urls import path
from store import views

urlpatterns = [
    path('product_list/',views.product_list,name='product_list' ),
    path('product/<int:id>/',views.product,name='product' ),
]