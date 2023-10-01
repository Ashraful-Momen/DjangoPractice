from django.shortcuts import render
import requests
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView


class SayHello(APIView):
        @method_decorator(cache_page(10*60))
        def get(self,request):
            response = requests.get('https://httpbin.org/delay/2')
            data = response.json()
            return render(request, 'hello.html', {'name': data})







