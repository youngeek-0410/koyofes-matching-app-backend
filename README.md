# Koyofes Matching App
こうよう祭2022用のマッチングアプリです。

# Usage
1. `docker-compose up -d`
   if logs directory doesn't exist, create it
1. `docker-compose run fastapi poetry run python manage.py collectstatic --noinput`
1. `docker-compose run fastapi poetry run python manage.py migrate`
1. `docker-compose run fastapi poetry run python manage.py createsuperuser`
