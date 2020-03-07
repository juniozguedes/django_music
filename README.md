'''Build docker'''
sudo docker-compose up -d --build

'''Migration'''
 sudo docker exec -i -t django_music_web_1 /bin/sh
 python manage.py migrate

'''Web server'''
http://0.0.0.0:8000/


sudo docker-compose run web python manage.py migrate'