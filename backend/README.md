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

## Изменить порт

Изменить конфигурационный файл [gunicorn.py](./gunicorn.py)
```python
from multiprocessing import cpu_count

bind = '0.0.0.0:<Указать порт>'
timeouts = 60
max_requests = 1000
workers = cpu_count()

reload = True
name = 'ichd_web'
```
    
Открыть порт в [docker-compose.prod.yml](../docker-compose.prod.yml)

```yaml
...
ichd_web:
 container_name: ichd_web
 build: ./backend
 ports:
   - <Указать порт>:<Указать порт>
 command: sh -c "gunicorn -c gunicorn.py backend.wsgi"
 restart: always
 env_file:
   - ./backend/.env
...
```