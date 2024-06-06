# falsk-test

Before start ensure you have docker installed x)
~~~
git clone https://github.com/Maytreyaya/flask-test-project
cd flask-test-project
docker-compose up --build

# inside the conteiner
    docker-compose exec web flask db init
    docker-compose exec web flask db migrate
    docker-compose exec web flask db upgrade

# to upload dump data into mysql db
mysql -u username -p password database_name < dump_file.sql


~~~