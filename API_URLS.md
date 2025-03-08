API сервера позволяет управлять пользователями, постами, комментариями и пользовательскими проектами. Ниже представлено описание доступных эндпоинтов и их функций.

/api/

1. **/register/ (POST)**
   - **POST**: Создает нового пользователя. Входные данные — JSON с полями name, email, password. Выходные данные — JSON с access и refresh токеном.
   {
    "refresh": "asdasd",
    "access": "asdasd"
   }

2. **/token (GET)**
   - **GET**: Возвращает access и refresh токен пользователя. Входные данные email и password. Выходные данные — JSON с access и refresh токеном.
   Входные данные
   {
    "email": "bulat",
    "password": "asdasd"
   }
   Выходные
   {
    "refresh": "asdasd",
    "access": "asdasd"
   }

3. **/token/refresh/ (POST)**
   - **POST**: Обновляет access токен. Входные данные — JSON с полями email и password, refresh. Выходные данные — JSON с access токеном.
   {
      "refresh": "sdfsdf"
   }
   Выход
   {
      "access": "sdfsfsf"
   }

4. **/projects/ (GET)**
   - **GET**: Возвращает список всех проектов. Входные данные access токен. Выходные данные — JSON со списком проектов.


5. **/user-projects/ (GET, PUT, DELETE)**
   - **GET**: Возвращает список пользовательских проектов. Входные данные access токен. Выходные данные — JSON со списком проектов пользователя.
   - **POST**: есть но его уберу потом он не нужен
   - **PUT**: /{id проекта}/
   

6. **/user_projects/{id}/ (GET, PUT, DELETE)**
   - **GET**: Возвращает пользовательский проект с переданным id. Входные данные access токен. Выходные данные — JSON проектом пользователя.
   - **PUT**: Обновляет информацию о пользовательском проекте. Входные данные — JSON с изменяемыми полями (code, is_published, earned_stars, language) и access токен. Выходные данные — JSON с обновленным проектом.
   - **DELETE**: Удаляет проект пользователя из таблицы userProjects. Входные данные - access токен. Выходные ничего если успешно,
   Если не успешно
   {
      "detail": "No UserProject matches the given query."
   }

7. **/user_projects/{id}/end_project/ (PUT)**
   - **PUT**: Завершает проект пользователя и устанавливает дату завершения. Входные данные id проекта передается в запросе. Выходные данные — JSON с обновленным статусом проекта или сообщением о том что проект завершить нельзя.

8. **/user_projects/start_project/ (POST)**
   - **POST**: Начинает новый проект для пользователя при соблюдении условий. Входные данные — JSON с project_id. Выходные данные — JSON с созданным проектом или сообщением об ошибке
   {
    "project_id": 1
   }
   Выход
   {
    "project_id": 1,
    "project_name": "Массивы",
    "code": "",
    "is_completed": false,
    "is_published": false,
    "earned_stars": 0,
    "language": null,
    "finished_date": null
   }  

7. **/map/connection/ (GET)**
   - **GET**: Возвращает соединения проектов на карте. Входных данных нет. Выходные данные — JSON с полями project, prev_project
[
    {
        "project": 1,
        "prev_project": null
    },
    {
        "project": 2,
        "prev_project": 1
    },
]

7. **/map/elements/ (GET)**
   - **GET**: Возвращает информацию о проектах на карте. Входных данных нет. Выходные данные — JSON с полями project_id, position_x, position_y, name, description, experience, coins
[
    {
      "project_id": 1,
      "position_x": 1.0,
      "position_y": 1.0,
      "name": "Массивы",
      "description": "Описание массивов",
      "experience": null,
      "coins": null
    },
    {
      "project_id": 2,
      "position_x": 10.0,
      "position_y": 1.0,
      "name": "Матрицы",
      "description": "Описание матрицы",
      "experience": null,
      "coins": null
    },
]

7. **/map/user-project-map/ (GET)**
   - **GET**: Возвращает информацию об открытых проектах пользователя. Входных данные access токен. Выходные данные — JSON с полями project_id, is_open, is_completed
[
   {
      "project_id": 1,
      "is_open": true,
      "is_completed": true
   },
   {
      "project_id": 2,
      "is_open": true,
      "is_completed": false
   },
]