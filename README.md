# Онлайн выставка котят

## Описание проекта
Проект представляет собой REST API для онлайн выставки котят, который позволяет пользователям добавлять, изменять, удалять и просматривать котят различных пород, а также оценивать их. API поддерживает JWT авторизацию для работы с пользователями. Приложение использует Django и Django Rest Framework для реализации функциональности.

## Основные возможности:
- Получение списка пород.
- Получение списка всех котят.
- Фильтрация котят по породе.
- Получение подробной информации о котенке.
- Добавление, изменение и удаление информации о котенке (доступно только владельцу котенка).
- JWT авторизация для защиты ресурсов.
- Оценка котят (от 1 до 5) другими пользователями.

## Установка и запуск приложения
### Системные требования
- Docker
- Docker Compose

### Шаги установки
1) Клонируйте репозиторий с GitHub:  
```git clone https://github.com/Stanis4live/Kittens.git```  
```cd Kittens```
2) Создайте .env файл, используя пример .env.sample:  
```cp .env.sample .env```
3) Соберите и запустите проект с помощью Docker Compose:  
```docker-compose up --build```
4) Приложение будет доступно по адресу: http://localhost:8000

### API документация
Документация API доступна в формате Swagger:
- Swagger: http://localhost:8000/api/docs/swagger/
- ReDoc: http://localhost:8000/api/docs/redoc/

## Возможности приложения

### Регистрация
Для регистрации нового пользователя необходимо отправить запрос на создание пользователя: http://localhost:8000/api/v1/user/register/
```
{
  "username": "ваше_имя",
  "password": "ваш_пароль",
  "email": "ваш_email"
}
```

### Авторизация
Для получения и обновления данных API необходимо пройти авторизацию с помощью JWT. Авторизация выполняется путем отправки запроса на получение токенов:
http://localhost:8000/api/token/
```
{
    "username": "ваше_имя",
    "password": "ваш_пароль"
}
```
В ответе вы получите access и refresh токены. Далее необходимо использовать access токен для авторизации в API.

### Основные эндпоинты
- Список пород:
GET ```/api/v1/exhibition/breeds/```  

- Список всех котят:
GET ```/api/v1/exhibition/kittens/```  

- Фильтрация котят по породе:
GET ```/api/v1/exhibition/kittens/?breed=scottish```

- Просмотр котенка:
GET ```/api/v1/exhibition/kittens/{id}/```

- Добавление котенка:
POST ```/api/v1/exhibition/manage-kittens/```

- Изменение котенка (доступно только владельцу):
PATCH ```/api/v1/exhibition/manage-kittens/{id}/```

- Удаление котенка (доступно только владельцу):
DELETE ```/api/v1/exhibition/manage-kittens/{id}/```

- Оценка котенка:
POST ```/api/v1/exhibition/rating/```

## Тестирование
Для проверки работоспособности функционала, в проекте реализованы тесты с использованием библиотеки pytest.

### Запуск тестов:
Выполните команду для запуска тестов: ```docker-compose exec web pytest -s```  

Все тесты покрывают основные сценарии работы с API: авторизация, создание, изменение, удаление котят, фильтрация, а также возможность оценки котят другими пользователями.

## Контейнеризация
Проект обернут в Docker, что позволяет быстро развернуть его на любой системе без необходимости ручной настройки окружения.

### Docker Compose
Файл ```docker-compose.yml``` включает в себя настройки для запуска двух контейнеров:

- **db:** контейнер с PostgreSQL базой данных.
- **web:** контейнер с Django приложением, который запускает Gunicorn сервер

## Заключение
Проект предоставляет REST API для выставки котят с JWT авторизацией и возможностью оценивания котят другими пользователями. Приложение легко разворачивается с помощью Docker и включает тесты для проверки основных функций.