Переходим в папку проекта

python -m venv venv
venv\Scripts\activate

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata fixtures/pmap.json
python manage.py loaddata fixtures/pposition.json
python manage.py loaddata fixtures/projects.json
python manage.py loaddata fixtures/users.json

python manage.py runserver