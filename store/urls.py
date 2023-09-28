from django.urls import path
from store import views
#default router show the api endpoint urls.
from rest_framework_nested import routers


app_name = 'store'


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet, basename='product') #assertions baseName error that's why add base name
router.register(r'collection', views.CollectionViewSet)
router.register(r'cart',views.CartViewSet,basename='cart')
router.register(r'customer', views.CustomerViewSet, basename='customer')
router.register(r'order', views.OrderViewSet, basename='order')

#for retrive reviews form product use => 
product_router = routers.NestedDefaultRouter(router, r'product', lookup='product')
product_router.register(r'review', views.ReviewViewSet, basename='product-reviews')
product_router.register(r'images',views.ProductIamgeViewSet, basename='images')

#for retrive cartItem form cart use=> 
cart_router = routers.NestedDefaultRouter(router, r'cart', lookup='cart') # send to cart_pk to CartItemViews.
cart_router.register(r'cartItem', views.CartItemViewSet, basename='cart-items') #basename has 2 route cart-item-detials/ cart-item-list #as nested routers

urlpatterns = [] + router.urls + product_router.urls + cart_router.urls 
