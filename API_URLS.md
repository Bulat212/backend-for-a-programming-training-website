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
   - **GET**: Возвращает минимальную информацию об открытых проектах пользователя. Входные данные access токен. Выходные данные — JSON с полями username, coins, stars, photo, nickname_id
   {
    "username": string,
    "coins": int,
    "stars": int,
    "photo": "http://127.0.0.1:8000/media/profile_pictures/image313.png",
    "nickname_id": int, 0 если нет активного ника
   }

14. **/shop/ (GET)**
   - **GET**: Возвращает информацию о стилях. Выходные данные — JSON с полями name, price_in_coin , price_in_stars, category
   
   [
      {
         "name": string,
         "price_in_coin": int,
         "price_in_stars": int,
         "category": int
      },
   ]

15. **/shop/id/ (GET)**
   - **GET**: Возвращает информацию о стиле с конкретным id. Выходные данные — JSON с полями name, price_in_coin , price_in_stars, category
   {
      "name": string,
      "price_in_coin": int,
      "price_in_stars": int,
      "category": int
   }

16. **/shop/? (GET)**
   После вопросительного знака можно вставить следующее:
   - price_in_stars__lt=10   фильтрация по цене за звезды меньше 10
   - price_in_stars__gt=10   фильтрация по цене за звезды больше 10
   - price_in_coin__gt=10    фильтрация по цене за коины больше 10
   - price_in_coin__lt=10    фильтрация по цене за коины меньше 10
   - category=nickname       фильтрация по названию категории nickname


17. **/userstyle/ (GET, POST)** авторизован
   - **GET**: Возвращает информацию о стилях юзера. Выходные данные — JSON с полями style, is_active
   - **POST**: Добавляет новую запись в таблицу UserStyle.(допустим если человек купил в магазине стиль). Входные данные — JSON с полями style, is_active, currency. Выходные данные — JSON с полями style, is_active если стиль приобрелся и добавился в таблицу.
   Eсли стиль уже есть - "detail": "Этот стиль уже куплен."
   Если не хватает средств - "detail": "Не хватает средств."
   
   {
    "style": string,
    "is_active": bool,
    "currency": "stars" or "coins" в зависимости от того, за что покупает
   }

18. **/admin-list-map-project/ (GET)** админ
   - **GET**: Возвращает список проектов, которых нет на карте. Выходные данные — JSON с полями id, name
[
   {
      "id": 1,
      "name": "Массивы"
   },
   {
      "id": 4,
      "name": "База данных"
   },
]

19. **/admin-create-map/ (POST)** админ
   - **POST**: Добавляет размещенные проекты в таблицы ProjectPosition, ProjectMap проектов. 
   Входные данные JSON список из project_id, prev_project_id, position_x, position_y
   [
    {
      "project_id": 2,
      "prev_project_id": 1,
      "position_x": 124,
      "position_y": 123
    },
    {
      "project_id": 5,
      "prev_project_id": 2,
      "position_x": 14,
      "position_y": 111
    }
   ]

   Выходные данные — JSON с полями project_id, prev_project_id
   [
      {
         "project_id": 2,
         "prev_project_id": 1
      },
      {
         "project_id": 5,
         "prev_project_id": 2
      }
   ]

   Если разместить на позиции где уже есть проект, то выдаст ошибку
   {
      "non_field_errors": [
            "Позиция на карте уже занята."
      ]
   },
   Если передать id проекта которого нет, то выдаст ошибку
   {
      "non_field_errors": [
            "Проект с id=123 не найден."
      ]
   },

20. **/temporary-projects/ (GET)** авторизован
   - **Get**: Выдает список временных проектов. Выходные данные JSON с полями проекта id, name, description, time_remaining (оставшееся время жизни проекта), experience, difficulty, coins
   Либо вернется пустой список если нет временных проектов
   [
    {
      "id": int,
      "name": str,
      "description": str,
      "time_remaining": "Оставшееся время - 0 дней, 23 часов, 58 минут.", str
      "experience": int или null
      "difficulty": int или null
      "coins": int или null
    }
   ]

21. **/started-projects/ (GET)** авторизован
   - **Get**: Выдает список начатых проектов пользователя. Выходные данные JSON с полями проекта id, name, description, experience, difficulty, coins
   [
    {
      "id": int,
      "name": str,
      "description": str,
      "experience": int или null
      "difficulty": int или null
      "coins": int или null
    }
   ]

22. **/finished-projects/ (GET)** авторизован
   - **Get**: Выдает список завершенных проектов пользователя. Выходные данные JSON с полями проекта id, name, description, experience, difficulty, coins
   [
    {
      "id": int,
      "name": str,
      "description": str,
      "experience": int или null
      "difficulty": int или null
      "coins": int или null
    }
   ]


23. **/profile/ (GET)** авторизован
   - **Get**: Выдает информацию о пользователе. last_projects - список последних 5 выполненных проектов
{
    "id": int,
    "username": str,
    "description": str,
    "photo": null или "/media/profile_pictures/image313.png"
    "experience": int,
    "nickname_id": int,
    "background_profile": int,
    "last_projects": [
        {
            "project_id": int,
            "project_name": str
        }
    ]
}

24. **/user-graph/ (GET)** авторизован
   - **Get**: Выдает информацию о прогрессе юзера.
   [
    {
      "user": 2,
      "experience": 5,
      "date": "2025-03-25"
    },
    {
      "user": 2,
      "experience": 3,
      "date": "2025-03-20"
    },
   ]

25. **/experience-ranking/[period]/[limit]/ (GET)** 
   - **Get**: Выдает рейтинг юзеров по опыту. Вместо period можно указать week или month (string), limit - сколько юзеров выводить (int)
   [
    {
      "user__id": 2,
      "user__username": "bulat",
      "total_experience": 132
    },
    {
      "user__id": 1,
      "user__username": "root",
      "total_experience": 123
    }
]

26. **/stars-ranking/[period]/[limit]/ (GET)** 
   - **Get**: Выдает рейтинг юзеров по звездам. Вместо period можно указать week или month (string), limit - сколько юзеров выводить (int)
[
   {
      "user__id": 1,
      "user__username": "root",
      "total_stars": 123
   },
   {
      "user__id": 3,
      "user__username": "andrey",
      "total_stars": 123
   },
   {
      "user__id": 2,
      "user__username": "bulat",
      "total_stars": 12
   }
]