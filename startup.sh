#!/bin/bash
python manage.py migrate && python manage.py collectstatic && gunicorn --workers 2 ecm2434_coursework.wsgi