# Продуктовый помощник Foodgram

Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`.

## Особенности реализации

* Проект завернут в Docker-контейнеры;
* Образы foodgram_frontend и foodgram_backend запушены на DockerHub.

## Стек технологий:

* Python 3.7
* Django
* DRF
* Docker

## Как развернуть проект на сервере

1. Подключитесь удаленному серверу:
- ssh <USERNAME>@<IP_ADDRESS>
2. Установите docker на сервер:
- sudo apt install docker.io
3. Установите docker-compose на сервер:
- sudo curl -L "https://github.com/docker/compose/releases/download/2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
- sudo chmod +x /usr/local/bin/docker-compose
4. Скопируйте подготовленные файлы из корневой папки проекта на сервер:
- scp docker-compose.yml username@host:/home/username/docker-compose.yml
- scp nginx.conf username@host:/home/username/nginx.conf
5. Выполните команду:
- sudo docker-compose up -d --build
6. Выполните миграции:
- sudo docker-compose exec backend python manage.py makemigrations
- sudo docker-compose exec backend python manage.py migrate
7. Соберите статику:
- sudo docker-compose exec backend python manage.py collectstatic --no-input
8. Заполните базу ингредиентами:
- sudo docker-compose exec backend python manage.py load_data
9. Создайте суперюзера:
- sudo docker-compose exec backend python manage.py createsuperuser

**Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**

## Автор
 [Латышева Виктория](https://github.com/vikkilat) 
