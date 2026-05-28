#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@bestcars.com', 'admin123')
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@bestcars.com', 'testpass123')
"
