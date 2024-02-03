#!/bin/bash

python manage.py migrate --noinput
gunicorn --bind ":8000" wallet_api.wsgi:application
