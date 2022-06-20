"""ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

envstate = os.getenv("ENV_STATE", "production")
if envstate == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
elif envstate == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")


application = get_asgi_application()


"""
FastAPI settings
"""
from matching.routers import user_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

fastapp = FastAPI()
fastapp.include_router(user_router, tags=["users"], prefix="/user")

# to mount Django
fastapp.mount("/django", application)
fastapp.mount("/static", StaticFiles(directory="static"), name="static")
