Переходим в папку проекта

python -m venv venv
venv\Scripts\activate

python manage.py makemigrations
python manage.py migrate
 
python manage.py loaddata fixtures/user.json projects.json Projectposition.json Userprojects.json Projectmap.json
python manage.py loaddata fixtures/user.json
python manage.py loaddata fixtures/projects.json
python manage.py loaddata fixtures/Projectposition.json
python manage.py loaddata fixtures/Userprojects.json
python manage.py loaddata fixtures/Projectmap.json


python manage.py runserver