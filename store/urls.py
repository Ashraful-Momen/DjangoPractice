from django.urls import path
from store import views
#default router show the api endpoint urls.
from rest_framework_nested import routers


app_name = 'store'


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product') #assertions baseName error that's why add base name
router.register(r'collection', views.CollectionViewSet)

product_router = routers.NestedDefaultRouter(router, r'product', lookup='product')
product_router.register(r'review', views.ReviewViewSet, basename='product-reviews')

urlpatterns = [] + router.urls + product_router.urls