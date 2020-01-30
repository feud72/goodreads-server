## Installation

```bash
python3 -m pip install pipenv

pipenv install --python $(which python3) --dev
```

## Setting

```bash
pipenv shell
python manage.py migrate
python manage.py seed_books
```

## Run on localhost
```bash
pipenv shell
python manage.py runserver 
or 
daphne -u daphne.sock -p 8000 config.asgi:application
```

## API


