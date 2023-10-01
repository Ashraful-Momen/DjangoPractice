from locust import HttpUser,task,between
from random import randint


class WebsiteUser(HttpUser):
    #view products
    #views product details
    # add product to cart

    wait_time = between(1,5) #waiting time is (1sec,5sec):

    @task(4) #we can use this task_number as our wish. 
    def view_products(self):
        print('view products')

        collection_id = randint(1,10)
        self.client.get(f'/store/product/?collection_id={collection_id}', name='/store/product') #want to show dirrent type fo collections products , that's why use randint.
        #product has a FK with collections_id , that why we can use => /store/product/?collection_id=2.(find the collections id of the product.)

    @task(2)
    def view_product(self): #single product.
        print('view products details')
        product_id = randint(1,999)
        self.client.get(f'/store/product/{product_id}', name='/store/product/:id')


    @task(1)
    def add_to_cart(self): # here cart_id value comes from 'def on_start':
        print('add to cart')
        product_id = randint(1, 10)
        self.client.get(f'/store/cart/{self.cart_id}/cartItem/',
                        name='/store/cart/cartItem',
                        json={
                            'product_id': product_id,
                            'quantity': 1
                        })


    #it's call everytime to new user to browse our website, it's not task , life cycle hood:
    def on_start(self):
        response = self.client.post(f'/store/cart/')
        result = response.json()
        self.cart_id = result['id']

    

    

