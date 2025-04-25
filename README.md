Переходим в папку проекта


python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
 
python manage.py loaddata fixtures/users.json fixtures/projects.json fixtures/languages.json fixtures/projectlanguages.json fixtures/Userprojects.json fixtures/Category.json fixtures/styles.json fixtures/userstyles.json fixtures/ProgressLog.json fixtures/UserProgress.json fixtures/userskills.json fixtures/comments.json fixtures/likes.json


python manage.py runserver


для себя
manage.py dumpdata style.Style > fixtures/styles.json