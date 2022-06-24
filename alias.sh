#!/bin/sh

# alias settings
alias build='docker-compose build'
alias up='docker-compose up'
alias stop='docker-compose stop'
alias down='docker-compose down'
alias upd='docker-compose up -d' # up with detached mode(background)

alias makemigrations='docker-compose run fastapi poetry run python manage.py makemigrations'
alias migrate='docker-compose run fastapi poetry run python manage.py migrate'
alias createsuperuser='docker-compose run fastapi poetry run python manage.py createsuperuser'
alias lessfastapilog='docker-compose run fastapi less /var/log/fastapi.log'
alias catfastapilog='docker-compose run fastapi cat /var/log/fastapi.log'
