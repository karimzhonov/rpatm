# Backend часть

## .env файл

    DEBUG=<1 - development, 0 - production> 
    SECRET_KEY=<Секретный ключ>
    
    POSTGRES_DB=<Название базы данных>
    POSTGRES_USER=<Username для базы данных>
    POSTGRES_PASSWORD=<Пароль для базы данных>
    POSTGRES_HOST=<Название хост который крутится база данных>
    POSTGRES_PORT=<Порт>

## Создание файли для логирование

В этой папке создать папка `logs` и внутри него создать 3 файла `error.log`, `warning.log`, `critical.log`

 * [...]()
 * [logs]()
   * [error.log]()
   * [warning.log]()
   * [critical.log]()
 * [...]()
 * [manage.py](./manage.py)

## Собрать статические файлы

    docker exec -it ichd_web python manage.py collectstatic

## Миграция

Создание миграции

    docker exec -it ichd_web python manage.py makemigrations

Применение миррации

    docker exec -it ichd_web python manage.py migrate

Создание супер-пользователя

    docker exec -it ichd_web python manage.py createsuperuser

