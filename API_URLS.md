API сервера позволяет управлять пользователями, постами, комментариями и пользовательскими проектами. Ниже представлено описание доступных эндпоинтов и их функций.

/api/

**1. Регистрация**

 **1.1 /register/ (POST)**
   - **POST**: Создает нового пользователя. Входные данные — JSON с полями name, email, password. Выходные данные — JSON с access и refresh токеном.
   {
    "refresh": "string",
    "access": "string"
   }

**/1.2 token (GET)**
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

**1.3 /token/refresh/ (POST)**
   - **POST**: Обновляет access токен. Входные данные — JSON с полями email и password, refresh. Выходные данные — JSON с access токеном.
   {
      "refresh": "string"
   }
   Выход
   {
      "access": "string"
   }

**1.4 /token/verify/ (POST)**
   - **POST**: Проверяет валидный ли access токен. Входные данные access токен.
   В случае валидности вернет {}
   Если не валиден:
   {
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
   }



**2. Проекты пользователя**


**2.1 /user-projects/ (GET, PUT, DELETE)**
   - **GET**: Возвращает список пользовательских проектов. Входные данные access токен. Выходные данные — JSON со списком проектов пользователя.
   - **POST**: есть но его уберу потом он не нужен

**2.2 /user-projects/{id}/ (GET, PUT, DELETE)**
   - **GET**: Возвращает пользовательский проект с переданным id. Входные данные access токен. Выходные данные — JSON проектом пользователя.
   - **PUT**: Обновляет информацию о пользовательском проекте. Входные данные — JSON с изменяемыми полями (code, is_published, earned_stars, language) и access токен. Выходные данные — JSON с обновленным проектом.
   - **DELETE**: Удаляет проект пользователя из таблицы userProjects. Входные данные - access токен. Выходные ничего если успешно,
   Если не успешно
   {
      "detail": "No UserProject matches the given query."
   }

**2.3 /user-projects/{id}/end_project/ (PUT)**
   - **PUT**: Завершает проект пользователя и устанавливает дату завершения. Входные данные id проекта передается в запросе, project-id проекта, language - язык в виде compiler_name, code.  Выходные данные — JSON с обновленным статусом проекта или сообщением о том что проект завершить нельзя.
   Входные данные
   {
    "project":1,
    "code":"a=int(input())\nb=int(input())\nprint(a+b)",          
    "language":"python"                                
   }

   В случае не прохода тестов выведет ошибку
   {
    "Project completion status": "Failed"
   }
<!-- **2.4 /user-projects/start_project/ (POST)**
   - **POST**: Начинает новый проект для пользователя при соблюдении условий. Входные данные — JSON с project_id. Выходные данные — JSON с созданным проектом или сообщением об ошибке
   {
    "project_id": int
   }
   Выход
   {
    "project_id": int,
    "project_name": "string",
    "project_description": str,
    "project_theory": str,
    "code": "string",
    "is_completed": bool,
    "is_published": bool,
    "earned_stars": int,
    "language": null, или может быть "string"
    "finished_date": null
   }   -->

**2.4 /user-projects/get_user_project/ (POST)**
   - **POST**: Начинает новый проект для пользователя при соблюдении условий. Входные данные — JSON с project_id. Выходные данные — JSON с созданным проектом или сообщением об ошибке
   {
    "project_id": int
   }
   Выход
   {
    "user_project": int,
    "project_id": int,
    "project_name": "string",
    "project_description": str,
    "project_theory": str,
    "code": "string",
    "is_completed": bool,
    "is_published": bool,
    "earned_stars": int,
    "language": null, или может быть str,
    "available_languages": [
      {
         "name": "Python",
         "compiler_name": "python"
      },
      {
         "name": "C++",
         "compiler_name": "cpp"
      }
    ],
    "finished_date": null
   } 
   

**2.5 /started-projects/ (GET)** авторизован
   - **Get**: Выдает список начатых проектов пользователя. Выходные данные JSON с полями проекта id, name, description, experience, difficulty, coins
   [
    {
      "project_id": int,
      "name": str,
      "description": str,
      "experience": int или null
      "difficulty": int или null
      "coins": int или null,
      "earned_stars": int
    }
   ]

**2.6 /finished-projects/ (GET)** авторизован
   - **Get**: Выдает список завершенных проектов пользователя. Выходные данные JSON с полями проекта id, name, description, experience, difficulty, coins
   [
    {
      "project_id": int,
      "name": str,
      "description": str,
      "experience": int или null
      "difficulty": int или null
      "coins": int или null,
      "earned_stars": int
    }
   ]




**3. Карта**

**3.1 /map/connection/ (GET)**
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

**3.2 /map/elements/ (GET)**
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

**3.3 /map/user-project-map/ (GET)** авторизован
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

**3.4 /admin-list-map-project/ (GET)** админ
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

**3.5 /admin-create-map/ (POST)** админ
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




**4. Магазин**

**4.1 /shop/ (GET)**
   - **GET**: Возвращает информацию о стилях. Выходные данные — JSON с полями name, price_in_coin , price_in_stars, category
   
   [
      {
         "name": string,
         "price_in_coin": int,
         "price_in_stars": int,
         "category": int
      },
   ]

**4.2 /shop/id/ (GET)**
   - **GET**: Возвращает информацию о стиле с конкретным id. Выходные данные — JSON с полями name, price_in_coin , price_in_stars, category
   {
      "name": string,
      "price_in_coin": int,
      "price_in_stars": int,
      "category": int
   }

**4.3 /shop/? (GET)**
   После вопросительного знака можно вставить следующее:
   - price_in_stars__lt=10   фильтрация по цене за звезды меньше 10
   - price_in_stars__gt=10   фильтрация по цене за звезды больше 10
   - price_in_coin__gt=10    фильтрация по цене за коины больше 10
   - price_in_coin__lt=10    фильтрация по цене за коины меньше 10
   - category=nickname       фильтрация по названию категории nickname



**5. Стили пользователя**

**5.1 /userstyle/ (GET, POST)** авторизован
   - **GET**: Возвращает информацию о стилях юзера. Выходные данные — JSON с полями style, is_active, category
  [
   {
      "style_id": 2,
      "is_active": true,
      "category": "nickname"
   },
   {
      "style_id": 2,
      "is_active": false,
      "category": "nickname"
    },
  ]
   - **POST**: Добавляет новую запись в таблицу UserStyle.(допустим если человек купил в магазине стиль). Входные данные — JSON с полями style, is_active, currency. Выходные данные — JSON с полями style, is_active если стиль приобрелся и добавился в таблицу.
   Eсли стиль уже есть - "detail": "Этот стиль уже куплен."
   Если не хватает средств - "detail": "Не хватает средств."
   
   {
    "style_id":int,
    "is_active": bool,
    "currency": "stars" or "coins" в зависимости от того, за что покупает
   }


**5.2 /userstyle/<int:style_id>/(PUT)** авторизован
   - **PUT**: Обновляет стиль профиля или ника. Входных данные в url строке - id стиля который нужно активировать. Если у пользователя нет такого стиля выведет ошибку - "detail":"У пользователя нет такого стиля."
   Если успешно акивируется, то выведет следующее
   Пример запроса 
   PUT /userstyle/1/
   Вывод:
   {
    "style": str,
    "is_active": true
   }

   Если нужно выключить стиль у пользователя, то добавляем id=0 в url и передаем поле clear_category
   
   PUT /userstyle/0/
   Входные данные
   {
      "clear_category": "nickname" или "background_profile" смотря что хотим выключить
   }
   Выходные данные
   {
    "style": "Gold Shine",
    "is_active": false
   }
   Если такого активного стиля нет то выведет следующее
   {
    "detail": "У пользователя нет такого активного стиля."
   }


**6. Проекты**

**6.1 /projects/ (GET)**
   - **GET**: Возвращает список всех проектов. Входные данные access токен. Выходные данные — JSON со списком проектов.


**6.2 /temporary-projects/ (GET)** авторизован
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



**7. Информация о пользователе**

**7.1 /profile/ (GET, PUT)** авторизован
   - **GET**: Выдает информацию о пользователе. last_projects - список последних 5 выполненных проектов
   - **PUT**: Можно изменить информацию о пользователе. Поля которые можно менять: username, description, photo.

Пример GET запроса
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

**7.2 /profile/<int:id>/ (GET)** авторизован
   - **GET**: Выдает информацию о пользователе по id. last_projects - список последних 5 выполненных проектов
   Пример запроса GET /api/profile/1/
   {
    "id": 1,
    "username": "root",
    "description": "",
    "photo": "http://127.0.0.1:8000/media/profile_pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-12-19_104405.png",
    "experience": 0,
    "nickname_id": 3,
    "background_profile": 0,
    "last_projects": []
   }

**7.3 /user-graph/ (GET)** авторизован
   - **Get**: Выдает информацию о прогрессе юзера.
   [
    {
      "user": str,
      "experience": 5,
      "date": "2025-03-25"
    },
    {
      "user": str,
      "experience": 3,
      "date": "2025-03-20"
    },
   ]

**7.4 /user-skills/ (GET, POST)** авторизован
   - **GET**: Выдает список навыков пользователя вместе с опытом. 
   Вывод
[
   {
      "language": "Python",
      "experience": 0
   },
   {
      "language": "Java",
      "experience": 0
   },
   {
      "language": "C++",
      "experience": 0
   }
]

   - **POST**: Входные параметры - JSON с полями language, experience 
   Входные данные
   {
      "language": "Python",
      "experience": 1
   }

   Вывод
   {
      "language": "Python",
      "experience": 650
   }

   При неверных данных
   {
      "language": [
         "Объект с name=у не существует."
      ],
      "experience": [
         "Введите правильное число."
      ]
   }

**7.5 /usermininfo/ (GET)** авторизован
   - **GET**: Возвращает минимальную информацию об открытых проектах пользователя. Входные данные access токен. Выходные данные — JSON с полями username, coins, stars, photo, nickname_id, is_staff - если true то админ, если false то обычный юзер
   {
    "username": string,
    "coins": int,
    "stars": int,
    "photo": "http://127.0.0.1:8000/media/profile_pictures/image313.png",
    "nickname_id": int, 0 если нет активного ника,
    "is_staff": true
   }


**8. Рейтинг**

**8.1 /experience-ranking/<str:period>/<int:limit>/ (GET)** 
   - **Get**: Выдает рейтинг юзеров по опыту. Вместо period можно указать week, month или all_time (string), limit - сколько юзеров выводить (int)
{
   "users": [
      {
         "user_id": 3,
         "username": "andrey",
         "photo": null,
         "nickname_id": 0,
         "total_experience": 1032
      },
      {
         "user_id": 1,
         "username": "root",
         "photo": "http://127.0.0.1:8000/media/profile_pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-12-19_104405.png",
         "nickname_id": 3,
         "total_experience": 123
      }
   ],
   "current_user_ranking": {
      "user_id": 6,
      "username": "victor",
      "photo": "http://127.0.0.1:8000/media/profile_pictures/image_2025-04-07_21-39-05.png",
      "nickname_id": 0,
      "total_experience": 0,
      "position": 4
   }
}


**8.2 /stars-ranking/<str:period>/<int:limit>/ (GET)** 
   - **Get**: Выдает рейтинг юзеров по звездам. Вместо period можно указать week, month или all_time (string), limit - сколько юзеров выводить (int). users - список юзеров. current_user_ranking - текущий пользователь., если чел не зареганый то вернет current_user_ranking : null
{
   "users": [
      {
         "user_id": 3,
         "username": "andrey",
         "photo": null,
         "nickname_id": 0,
         "total_stars": 123
      },
      {
         "user_id": 1,
         "username": "root",
         "photo": "http://127.0.0.1:8000/media/profile_pictures/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2024-12-19_104405.png",
         "nickname_id": 3,
         "total_stars": 123
      }
   ],
   "current_user_ranking": {
      "user_id": 6,
      "username": "victor",
      "photo": "http://127.0.0.1:8000/media/profile_pictures/image_2025-04-07_21-39-05.png",
      "nickname_id": 0,
      "total_stars": 0,
      "position": 4
   }
}


**9. Комментарии**

**9.1 /comment/<int:pk>/ (GET)** 
   - **Get**: Выдает опубликованные коды к проекту и комментарии под ним. В параметр GET запроса нужно вводить id проекта из таблицы Project
   user - имя пользователя, который выложил свой код, project - название проекта, user_project - id из таблицы UserProject проекта который он выполнил, code - его код, earned_stars - заработанные звезды (лайки). comments - комментарии под кодом, user - человек который оставил комментарий, text - текст комментария
   Пример вывода. 
   [
      {
         "user": "bulat",
         "project": "Деревья",
         "user_project": "2",
         "code": "print(\"Деревья\")",
         "earned_stars": 0,
         "comments": [
            {
               "user": "andrey",
               "text": "а я по другому сделал"
            },
            {
               "user": "gena",
               "text": "круто"
            },
            {
               "user": "andrey",
               "text": "второй коммент"
            }
         ]
      },
      {
         "user": "victor",
         "project": "Деревья",
         "user_project": "3",
         "code": "print(\"Написал victor\")",
         "earned_stars": 0,
         "comments": [
            {
               "user": "bulat",
               "text": "этот коммент под виктора"
            }
         ]
      }
   ]

**9.2 /set-like/ (POST)** 
   - **POST**: Ставит лайк на выбранный проект пользователя. Вводные данные JSON с проектом юзера user_project_id
   Если лайк уже поставлен, то выдаст "error": "Нельзя повторно ставить лайки."
   Если выбран проект самого пользователя  "error": "Нельзя самому себе ставить лайки."

   Пример входных данных, где 1 - id проекта в таблице UserProject
   {
    "user_project_id": 1
   }
  
   Выходные данные? где "bulat - Массивы."- проект в таблице UserProject, user -кому ставят, liker - кто поставил, earned_stars - сколько теперь лайков на проекте
   {
    "message": "Лайк добавлен на bulat - Массивы.",
    "data": {
      "user": "bulat",
      "project": "Массивы",
      "earned_stars": 8,
      "liker": "root"
    }
   }

**9.3 /write-comment/ (POST)** авторизован
   - **POST**: Добавляет комментарий под чужой код. Входные данные JSON с полями user_project - id проекта пользователя под которым оставят комментарий, text - текст комментария
Пример ввода
{
    "user_project": 4,
    "text":"я булат и оставлю коммент под gena"
}

Пример вывода, где user- пользователь который оставляет комментарий:
{
    "user": "bulat",
    "user_project": 4,
    "text": "я булат и оставлю коммент под gena"
}


**10. Компилятор**

**10.1 /code-executor/ (POST)** авторизован
   - **POST**: Отправляет код на компиляцию. Входные данные - user_project - id проекта юзера из таблицы user_project, code, language, input_data(не обязательно), project

   {
      "user_project":1,
      "project":1,
      "input_data":"3\n6",
      "code":"a=int(input())\nb=int(input())\nprint(a+b)",
      "language":"python"
   }

   Успешный ответ
   {
      "output": "9\n",
      "status": "Accepted"
   }
   Ответ с ошибкой
   {
    "output": "Traceback (most recent call last):\n  File \"script.py\", line 2, in<module>\n b=int(input())\nValueError: invalid literal for int() with base 10: 's'\n",
    "status": "Runtime Error (NZEC)"
   }

**10.1 /code-executor/check-solution/ (POST)** авторизован
   - **POST**: Отправляет код на проверку. Входные данные - user_project - id проекта юзера из таблицы user_project, code, language, project
Пример входных данных
   {
      "user_project":1,
      "project":1,
      "code":"a=int(input())\nb=int(input())\nprint(a+b)",
      "language":"python"
   }

   Пример упешного вывода
   {
    "status": True
   }
   Пример ошибки
   {
    "output": "Traceback (most recent call last):\n  File \"script.py\", line 3, in <module>\n    print(a+b)\nTypeError: can only concatenate str (not \"int\") to str\n",
    "status": False
   }