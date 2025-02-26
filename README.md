Переходим в папку проекта

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

manage.py loaddata fixtures/pmap.json
manage.py loaddata fixtures/pposition.json
manage.py loaddata fixtures/projects.json
manage.py loaddata fixtures/users.json

python manage.py runserver