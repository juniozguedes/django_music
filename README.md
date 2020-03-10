'''Build docker'''
sudo docker-compose up -d --build

'''Migration'''
 sudo docker-compose run  web python manage.py migrate

'''Web server'''
http://0.0.0.0:8000/