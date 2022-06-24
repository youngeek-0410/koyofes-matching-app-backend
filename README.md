# Koyofes Matching App
こうよう祭2022用のマッチングアプリです。

# Usage
1. `docker-compose up -d`
2. `docker-compose run fastapi poetry run python manage.py collectstatic --noinput`
3. `docker-compose run fastapi poetry run python manage.py migrate`
4. `docker-compose run fastapi poetry run python manage.py createsuperuser`
