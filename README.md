# flask-test

Before start ensure you have docker installed x)
~~~ sh
git clone https://github.com/Maytreyaya/flask-test-project
cd flask-test-project
docker-compose up --build

~~~
The application uses JWT for authentication. To use methods that require authentication, obtain a JWT token.

### Obtaining a JWT token

Send a POST request to `/register` first and then `/login`:

```sh
curl -X POST http://localhost:5000/auth/register\
  -H "Content-Type: application/json" \
  -d '{"email": "yo@example.com", "password": "your_password", "roles": "admin"}'


curl -X POST http://localhost:5000/auth/login\
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@example.com", "password": "your_password"}'

```
Now you have access JWT Token
### To test work of the app and receive information about order

``` sh
# create product
curl -X POST http://localhost:5000/jsonrpc/jsonrpc \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxODEwNzM0MywianRpIjoiNTMxNWFlMjktMTk1YS00NDQ3LWFhYzEtZTEyNDEwZDFhN2ZhIiwidHlwZSI6ImFjY2VzcyIsInN1
YiI6NiwibmJmIjoxNzE4MTA3MzQzLCJjc3JmIjoiMjVlMDdmNjQtYmFiNS00NjkzLTlkMzMtMGIzNzZhMWY1NmY2IiwiZXhwIjoxNzE4MTEwOTQzfQ.39rdHQdjNa47zLryvq8jJEtuI4pLWCdQpd78JKO_eQ8""\
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "create_product",
    "params": {
        "name": "pupa",
        "price": "3.0",
        "weight": "10",
        "color": "red"
    },
    "id": 1
}'

# create adress
curl -X POST http://localhost:5000/jsonrpc/jsonrpc \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "create_address",
    "params": {
        "country": "Ukr",
        "city": "Vin",
        "street": "Sobor"
    },
    "id": 1
}'

# create order
curl -X POST http://localhost:5000/jsonrpc/jsonrpc \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "create_order",
    "params": {
        "order_items": [{
            "product_id": 1,
            "quantity": 2
        }],
        "address_id": 1,
        "status": "pending"
    },
    "id": 1
}'

# update order with celery logging
curl -X POST http://localhost:5000/jsonrpc/jsonrpc \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "update_order",
    "params": {
        "order_id": 1,
        "new_status": "paid"
    },
    "id": 1
}'

```