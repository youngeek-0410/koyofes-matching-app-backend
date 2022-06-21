# Koyofes Matching App
こうよう祭2022用のマッチングアプリです。

# Usage
1. `docker-compose up -d`

   if logs directory doesn't exist (`Error: Error: './logs/django_error.log' isn't writable [FileNotFoundError(2, 'No such file or directory')]`), create it (`fastapi/logs`)
2. `docker-compose run fastapi poetry run python manage.py collectstatic --noinput`
3. `docker-compose run fastapi poetry run python manage.py migrate`
4. `docker-compose run fastapi poetry run python manage.py createsuperuser`
