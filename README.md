# graphservice



run docker-compose up --build

docker exec  -it graphservice_web bash
python manage.py makemigrations
python manage.py migrate
