API сервера позволяет управлять пользователями, постами, комментариями и пользовательскими проектами. Ниже представлено описание доступных эндпоинтов и их функций.

/api/

1. **/register/ (POST)**
   - **POST**: Создает нового пользователя. Входные данные — JSON с полями name, email, password. Выходные данные — JSON с access и refresh токеном.
   {
    "refresh": "string",
    "access": "string"
   }

2. **/token (GET)**
   - **GET**: Возвращает access и refresh токен пользователя. Входные данные email и password. Выходные данные — JSON с access и refresh токеном.
   Входные данные
   {
    "email": "string",
    "password": "asdasd"
   }
   Выходные
   {
    "refresh": "string",
    "access": "string"
   }

3. **/token/refresh/ (POST)**
   - **POST**: Обновляет access токен. Входные данные — JSON с полями email и password, refresh. Выходные данные — JSON с access токеном.
   {
      "refresh": "string"
   }
   Выход
   {
      "access": "string"
   }

4. **/token/verify/ (POST)**
   - **POST**: Проверяет валидный ли access токен. Входные данные access токен.
   В случае валидности вернет {}
   Если не валиден:
   {
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
   }

5. **/projects/ (GET)**
   - **GET**: Возвращает список всех проектов. Входные данные access токен. Выходные данные — JSON со списком проектов.


6. **/user-projects/ (GET, PUT, DELETE)**
   - **GET**: Возвращает список пользовательских проектов. Входные данные access токен. Выходные данные — JSON со списком проектов пользователя.
   - **POST**: есть но его уберу потом он не нужен
   - **PUT**: /{id проекта}/
   

7. **/user_projects/{id}/ (GET, PUT, DELETE)**
   - **GET**: Возвращает пользовательский проект с переданным id. Входные данные access токен. Выходные данные — JSON проектом пользователя.
   - **PUT**: Обновляет информацию о пользовательском проекте. Входные данные — JSON с изменяемыми полями (code, is_published, earned_stars, language) и access токен. Выходные данные — JSON с обновленным проектом.
   - **DELETE**: Удаляет проект пользователя из таблицы userProjects. Входные данные - access токен. Выходные ничего если успешно,
   Если не успешно
   {
      "detail": "No UserProject matches the given query."
   }

8. **/user_projects/{id}/end_project/ (PUT)**
   - **PUT**: Завершает проект пользователя и устанавливает дату завершения. Входные данные id проекта передается в запросе. Выходные данные — JSON с обновленным статусом проекта или сообщением о том что проект завершить нельзя.

9. **/user_projects/start_project/ (POST)**
   - **POST**: Начинает новый проект для пользователя при соблюдении условий. Входные данные — JSON с project_id. Выходные данные — JSON с созданным проектом или сообщением об ошибке
   {
    "project_id": int
   }
   Выход
   {
    "project_id": int,
    "project_name": "string",
    "code": "string",
    "is_completed": bool,
    "is_published": bool,
    "earned_stars": int,
    "language": null, или может быть "string"
    "finished_date": null
   }  

10. **/map/connection/ (GET)**
   - **GET**: Возвращает соединения проектов на карте. Входных данных нет. Выходные данные — JSON с полями project, prev_project
[
    {
        "project": int,
        "prev_project": null
    },
    {
        "project": int,
        "prev_project": int
    },
]

11. **/map/elements/ (GET)**
   - **GET**: Возвращает информацию о проектах на карте. Входных данных нет. Выходные данные — JSON с полями project_id, position_x, position_y, name, description, experience, coins
[
    {
      "project_id": int,
      "position_x": float,
      "position_y": float,
      "name": "string",
      "description": "string",
      "experience": null, или int
      "coins": null или int
    },
    {
      "project_id": int,
      "position_x": float,
      "position_y": float,
      "name": "string",
      "description": "string",
      "experience": null, или int
      "coins": null или int
    },
]

12. **/map/user-project-map/ (GET)** авторизован
   - **GET**: Возвращает информацию об открытых проектах пользователя. Входных данные access токен. Выходные данные — JSON с полями project_id, is_open, is_completed
[
   {
      "project_id": int,
      "is_open": bool,
      "is_completed": bool
   },
   {
      "project_id": int,
      "is_open": bool,
      "is_completed": bool
   },
]

13. **/usermininfo/ (GET)** авторизован
   - **GET**: Возвращает минимальную информацию об открытых проектах пользователя. Входные данные access токен. Выходные данные — JSON с полями username, coins, stars, nickname_id
   {
    "username": string,
    "coins": int,
    "stars": int,
    "nickname_id": int, 0 если нет активного ника
   }

14. **/usermininfo/ (GET)**
   - **GET**: Возвращает информацию о стилях. Выходные данные — JSON с полями name, price_in_coin , price_in_stars, category
   {
      "name": string,
      "price_in_coin": int,
      "price_in_stars": int,
      "category": int
   },