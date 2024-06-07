# flask-test

Before start ensure you have docker installed x)
~~~ sh
git clone https://github.com/Maytreyaya/flask-test-project
cd flask-test-project
docker-compose up --build

# inside the conteiner in needed
    docker-compose exec web flask db init
    docker-compose exec web flask db migrate
    docker-compose exec web flask db upgrade

# to upload dump data into mysql db
mysql -u username -p password database_name < dump_file.sql
~~~
The application uses JWT for authentication. To use methods that require authentication, obtain a JWT token.

### Obtaining a JWT token

Send a POST request to `/register` first and then `/login`:

```sh
curl -X POST http://localhost:5000/register\
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@example.com", "password": "your_password", "roles":[]}'


curl -X POST http://localhost:5000/login\
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@example.com", "password": "your_password"}'

```
Now you have access JWT Token
To receive information about order(if it's present in db)

``` sh
curl -X POST http://localhost:5000/jsonrpc \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "get_order",
    "params": {"order_id": 1},
    "id": 1
}'
```