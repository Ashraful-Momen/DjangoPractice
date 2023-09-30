from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User

from rest_framework import status

@pytest.fixture
def api_client(): #this fixture works for end_api
    return APIClient


@pytest.fixture
def authenticate(api_client):# in api_client parameter we pass the authenticate_user.
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate
    













#chatgpt: -----------------------------------------------
# from rest_framework.test import APIClient
# import pytest
# from django.contrib.auth.models import User

# @pytest.fixture
# def api_client():
#     return APIClient()

# @pytest.fixture
# def authenticate(api_client):
#     def do_authenticate(is_staff=False):
#         user = User.objects.create(username='testuser', is_staff=is_staff)
#         api_client.force_authenticate(user=user)
#         return user
#     return do_authenticate


# ----------------------those code for test_collections_api.py----------------
# def test_authenticated_user(authenticate):
#     user = authenticate(is_staff=True)
#     response = api_client.get('/your-api-endpoint/')
#     assert response.status_code == 200
#     # Add more assertions based on the behavior of your view
