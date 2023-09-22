

from django.urls import path
from store import views

from rest_framework.routers import SimpleRouter,DefaultRouter #default router show the api endpoint urls.

app_name = 'store'


router = DefaultRouter()
router.register(r'product', views.ProductViewSet) 
router.register(r'collection', views.CollectionViewSet) 
urlpatterns = [] + router.urls


# from django.urls import path
# from store import views

# urlpatterns = [
#     path('product/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
#     path('product/<str:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
#     path('collections/', views.CollectionViewSet.as_view({'get': 'list', 'post': 'create'}), name='collection-list'),
#     path('collections/<int:pk>/', views.CollectionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='collection-detail'),
# ]







# ===============================================================================
 # path('product_list/', views.Product_list.as_view(),name='product_list'),
    # path('product/<str:sku>/', views.Product_details.as_view(), name='product_details'),
    # path('collections/<int:pk>/', views.collection, name='collection-detials'), # serializer method - 4 .

    # path('collections_list/',views.Collection_list.as_view(), name='collections'), 
    # path('collection/<int:pk>/',views.Collections_details.as_view(),name='collection_details'),  # Add a trailing slash
    # --------------------------------------------------------------

