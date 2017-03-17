# backend
Application backend serving a REST API

## How to install
    virtualenv3 --always-copy venv && source venv/bin/activate && pip install -r requirements.txt && python localizefriends/manage.py migrate

## How to run development server
    source venv/bin/activate && python localizefriends/manage.py runserver
