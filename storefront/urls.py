from django.contrib import admin
from django.urls import path, include
from playground import views
from store import views


admin.site.site_header = "StoreFront " #admin page heading 
admin.site.index_title = "Admin" #admin page title

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.product_list,name='index_page'),
    path('playground/', include('playground.urls')),
    path('store/', include('store.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
