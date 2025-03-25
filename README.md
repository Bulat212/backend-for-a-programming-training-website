Переходим в папку проекта


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
 
python manage.py loaddata fixtures/user.json fixtures/projects.json fixtures/Projectposition.json fixtures/Userprojects.json fixtures/Projectmap.json fixtures/Category.json fixtures/styles.json fixtures/UserStyle.json fixtures/ProgressLog.json fixtures/UserProgress.json
python manage.py loaddata fixtures/user.json
python manage.py loaddata fixtures/projects.json
python manage.py loaddata fixtures/Projectposition.json
python manage.py loaddata fixtures/Userprojects.json
python manage.py loaddata fixtures/Projectmap.json
python manage.py loaddata fixtures/Category.json
python manage.py loaddata fixtures/styles.json
python manage.py loaddata fixtures/UserStyle.json
python manage.py loaddata fixtures/ProgressLog.json
python manage.py loaddata fixtures/UserProgress.json


python manage.py runserver


для себя
manage.py dumpdata style.Style > fixtures/styles.json