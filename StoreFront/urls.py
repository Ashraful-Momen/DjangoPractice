
from django.contrib import admin
from django.urls import path,include
from playground import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('',views.say_hello,name='hello'),
    path("__debug__/", include("debug_toolbar.urls")),
]
