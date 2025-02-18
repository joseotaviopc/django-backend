#!/bin/bash
python -m venv venv

source venv/bin/activate

pip install django pillow django-ninja

python manage.py runserver