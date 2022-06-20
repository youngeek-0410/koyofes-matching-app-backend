# config
wsgi_app = "config.asgi:application"
worker_class = "config.worker.RestartableUvicornWorker"
bind = "0.0.0.0:8001"
workers = 1
reload = True
daemon = False  # not to finish process FIXME

# log
errorlog = "./logs/django_error.log"
accesslog = "/var/log/django_access.log"
