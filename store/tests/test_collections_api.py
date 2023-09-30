#(Arrange,Act,Assert): 
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from store.models import Collections,Products
from model_bakery import baker # for creating the models objects ,test purpose.
from rest_framework.test import APIClient



#create fixture for api_end_point: 
@pytest.fixture
def create_collection(api_client):

    def do_create_collection(collection):
        return api_client().post('/store/collection/', collection)
    # def do_create_collection(collection):#receive api {'title':'value'}
    #     return api_client.post('/store/collection',collection)
    return do_create_collection


@pytest.mark.django_db
class TestCreateCollections: 
    # @pytest.mark.skip    #for skip this test
    def test_if_user_anonimous_return_401(self,create_collection): #this api_client,collection from fixture.
        
        response = create_collection({'title':'a'}) #this function call from fixture
        
        assert response.status_code == status.HTTP_201_CREATED #check the bad request.
       


    def test_if_collections_is_created_201(self,create_collection):
        
        response = create_collection({'title':'a'}) #this function call from fixture
       

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        # assert response.status_code == status.HTTP_401_UNAUTHORIZED





# ======================================================
import pytest
from rest_framework import status
from store.models import Collections
from model_bakery import baker

@pytest.mark.django_db
class TestRetriveCollection():
    def test_is_collection_exit_return_200(self, api_client):
        # Create a collection using model_bakery
        collection = baker.make(Collections)

        # Make a GET request to retrieve the collection
        response = api_client().get(f'/store/collection/{collection.id}/') #if we miss '/' end of the api url , error : 301. 

        # Check if the response status code is 200 OK
        assert response.status_code == status.HTTP_200_OK

        # Check if the response data matches the expected values
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0  # Assuming products_count is expected to be 0
        }

 # collection = baker.make(Collections) #make collections object for model .
        # baker.make(Products,collection=collection, _quantity=10) #create 10 product for 1 collections.

        # assert False