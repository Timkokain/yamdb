# api_yamdb
## Ver 1.05

![example workflow](https://github.com/github/docs/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание

Проект YaMDb собирает отзывы пользователей на различные произведения.

## Как yamdb работает

Позволяет взаимодействовать с эндпоинтами api_yamdb посредством отправки и получения стандартных json GET, POST, PUT, PATCH, DELETE запросов.
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором.
Хранятся только ревью на произведения. В каждой категории есть произведения. Произведению может быть присвоен жанр.
Любой пользователь может оставить к произведениям текстовые отзывы и оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Установка
### Что необходимо для локального использования:

Для работы необходимо установить [Docker](https://www.docker.com/)

## Запуск

Приложение разделено на 3 контейнера:
* db - база данных postgresql
* web - основное приложение где расположен django manage.py
* nginx - раздача статики и картинок.

&#x1F534; Для работы <ins>обязательно</ins> в директории /infra создать .env (пример в .env_example)

После запуска проект доступен по адресу http://localhost/

Готовый docker api_yamdb можно запулить:
```bash
 docker pull timkokain/yamdb
```
Исполнение команд производится в директории /infra
* Для сборки образа и запуска контейнеров:
```bash
docker-compose up
```
* Что-бы пересобрать контейнеры после внесенных изменений:
```bash
docker-compose up -d --build
```
* Остановить все контейнеры:
```bash
docker-compose stop
```
* Исполнение manage.py команд проводится через:
```bash
docker-compose exec web python manage.py <command>
```
### Для начала работы необходимо (контейнеры должны быть запущены)
  - выболнить миграции:
  ```bash
  docker-compose exec web python manage.py migrate
  ```
  - загрузить фикстуры:
  ```bash
  docker-compose exec web python manage.py load_data
  ```
  - собрать статику:
  ```bash
  docker-compose exec web python manage.py colectstatic --no-input
  ```
  - если необходимо, создайте суперпользователя:
  ```bash
  docker-compose exec web python manage.py createsuperuser
  ```
  - заполнить базу данными:
  ```bash
  cat fixture.json | docker exec -i web python manage.py loaddata --format=json
  ```
### Дополнительно
* Посмотреть логи контейнера:
```bash
docker logs --follow <container_name>
```
  - Все запущенные контейнеры:
  ```bash
  docker container ls
  ```
* Подсоединиться к контейнеру (bash):
```bash
# если операционная стема windows
winpty docker exec -it <container_name> bash
# если операционная стема linux
docker exec -it <container_name> bash
```

Если хочется чего то особенного вам поможет [Docker.docks](https://docs.docker.com/)
# Приложение yamdb
## Пользователи и их права доступа
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.

Для всего остального необходима аутентификация и получение токена авторизации:
* Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт `/api/v1/auth/signup/`
* Получение токена методом POST по адресу `.../auth/jwt/create/`
payload body:
```json
{
    "email": "email@admin.com",
    "username ": "12345"
}
```
* Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
* Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен):
response:
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2MTg3NDIzLCJpYXQiOjE2NjM1OTU0MjMsImp0aSI6ImViMjJhMzZlMzFlNzRiYjBiMzY5NzEwNTUxYTJiMTM0IiwidXNlcl9pZCI6MX0.w6ZyeignRuxdZpZ-lfqkQ2xuNg33jSpPTEkxtW2ZbXY"
}
```

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. Время действия токена можно менять в settings.

* `/api/v1/users/me/` - личная "страница" пользователя. Пользователь может заполнить страницу о себе отправив POST запрос.
Роли пользователей может менять только пользователь с ролью "admin".

### Основные эндпоинты
- "auth": "http://***/api/v1/auth/"
- "categories": "http://***/api/v1/categories/"
- "genres": "http://***/api/v1/genres/"
- "titles": "http://***/api/v1/titles/"
- "reviews": "http://***/api/v1/titles/{title_id}/reviews/"
- "comments": "http://***/api/v1/titles/{title_id}/reviews/{review_id}/comments/"

## Примеры запросов
- GET `.../api/v1/categories/`
response:
```json
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
]
```

- POST `.../api/v1/genres/`
payload body:
```json
{
   "name": "string",
   "slug": "string"
}
```

- PATCH  `.../api/v1/titles/{titles_id}/`
payload body:
```json
{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
    "string"
    ],
    "category": "string"
}
```
response:
```json
{
    "id": 0,
    "name": "string",
    "year": 0,
    "rating": 0,
    "description": "string",
    "genre": [
        {
            "name": "string",
            "slug": "string"
        }
    ],
    "category": {
        "name": "string",
        "slug": "string"
    }
}
```

- POST `...api/v1/titles/{title_id}/reviews/`
payload body:
```json
{
  "text": "string",
  "score": 5
}
```
response:
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 5,
  "pub_date": "2022-09-19T12:50:18.792634Z "
}
```

- PATCH `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`
payload body:
```json
{
    "text": "string"
}
```
response:
```json
{
    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2022-09-19T12:50:18.792634Z "
}
```


## Авторы

* Timkoakin
* VladPetukhin
* morgin3
## License

Opensorce
