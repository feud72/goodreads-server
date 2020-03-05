## Prerequisite

### Kakao Developer

```
https://developers.kakao.com
```

#### Create App

```
https://developers.kakao.com/apps/new
```

#### Get REST API KEY

```
https://developers.kakao.com/apps/{{ YOUR APP }}/settings/general

Save it on .env > KAKAO_ID
```

#### Set Login Redirect URI

```
https://developers.kakao.com/apps/{{ YOUR APP }}/settings/user

Base URL should be same as .env > API_URI
```

### 도서관 정보나루

#### Get API KEY

```
https://www.data4library.kr/apiUtilization

Save it on .env > LIB_KEY
```

## Installation

```bash
pip install pipenv

pipenv install --python $(which python3) --dev
```

## Setting

```bash
pipenv shell
python manage.py migrate
```

### .env

```
KAKAO_ID = {{ YOUR KAKAO API_APP_KEY }} // NEVER POST THIS IN PUBLIC
API_URI = "http://127.0.0.1:8000"
LIB_BASE_URL = "http://data4library.kr/api/"
LIB_KEY = "{{ YOUR LIBRARY API_KEY }}" // NEVER POST THIS IN PUBLIC

DJANGO_SECRET_KEY = "{{ YOUR DJANGO SECRET KEY }}" // NEVER POST THIS IN PUBLIC
DJANGO_WEBSERVER_DB_ENGINE = "django.db.backends.postgresql_psycopg2"
DJANGO_WEBSERVER_DB_NAME = "{{ YOUR DB NAME }}"
DJANGO_WEBSERVER_DB_USER = "{{ YOUR DB USER }}"
DJANGO_WEBSERVER_DB_PASSWORD = "{{ YOUR DB PASSWORD }}" // NEVER POST THIS IN PUBLIC
DJANGO_WEBSERVER_DB_HOST = "{{ YOUR DB HOST }}"
DJANGO_WEBSERVER_DB_PORT = "{{ YOUR DB PORT }}"

AWS_REGION = "{{ YOUR AWS REGION ex. ap-northeast-2}}"
AWS_STORAGE_BUCKET_NAME = "{{ YOUR AWS S3 BUCKET NAME }}"
AWS_ACCESS_KEY_ID = "YOUR AWS ACCESS KEY " // NEVER POST THIS IN PUBLIC
AWS_SECRET_ACCESS_KEY = "YOUR AWS SECRET ACCESS KEY" // NEVER POST THIS IN PUBLIC
```

### Amazon Web Service (AWS)

```
You should have an AWS account, and use S3 bucket.

If you want to run in a different environment, you need to modify 'config/base.py' file.
```

### Docker and docker-compose

```
https://docs.docker.com/compose/install/
```

## Run 

### Prerequisite

- Dev environment

```python3
from .base import *
from .dev import *
```

- Production environment

```python3
from .base import *
from .aws import *
```


### on localhost
```bash
pipenv shell
python manage.py runserver 
```

## API


