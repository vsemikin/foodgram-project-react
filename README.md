### О проекте:

Cайт Foodgram, «Продуктовый помощник». На этом сайте пользователи могут  публиковать рецепты, подписываться на публикации других пользователей,  добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин  
скачивать сводный список продуктов, необходимых для приготовления  одного или нескольких выбранных блюд.

### Docker для Ubuntu:

Инструкция по установке Docker:

https://docs.docker.com/engine/install/ubuntu/

### Что должен содержать файл .env:

Файл .env содержит переменные окружения для работы с базой данных:

```yaml
DJANGO_SECRET_KEY # секретный ключ проекта
DJANGO_ALLOWED_HOSTS # список хостов для обслуживания проектом в формате:  <host1, host2, host3>
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к БД
DB_HOST # название контейнера
DB_PORT # порт для подключения к БД
```

### Запуск проекта:

Для запуска проекта необходимо перейти в директорию  
/foodgram-project-react/infra и выполнить команду:

```bash
docker-compose up
```

Пересобрать проект:

```bash
docker-compose up --build
```

Остановка:

```bash
docker-compose down
```

### Команды для docker:

Список контейнеров с информацией о них:

```bash
docker ps
```

Вход в контейнер:

```bash
docker exec -it <CONTAINER ID> bash
```

Находясь в контейнере провести миграции, сформировать базу и  
собрать статику:

```bash
python manage.py makemigrations # миграции
python manage.py migrate # создать таблицы базы данных из миграций
python manage.py collectstatic # собрать статику для панели администратора
```

### Технологии проекта:

* Python
* Django
* PostgreSQL
* Docker
* NGINX
* GitHub

### Об авторе:

Семикин Владимир, студент 16 когорты факультета Бэкенд Яндекс Практикум.
