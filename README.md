## API Documentation

### [API Link](https://github.com/feud72/goodreads-server/blob/master/api.md)

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

### .env

**Caution** : docker-compose 환경의 .env 파일은 쌍따옴표(")가 들어가면 안됩니다.

```
KAKAO_ID={{ YOUR KAKAO API_APP_KEY }} // NEVER POST THIS IN PUBLIC
API_URI=http://127.0.0.1:8000
LIB_BASE_URL=http://data4library.kr/api/
LIB_KEY={{ YOUR LIBRARY API_KEY }} // NEVER POST THIS IN PUBLIC

DJANGO_SECRET_KEY={{ YOUR DJANGO SECRET KEY }} // NEVER POST THIS IN PUBLIC
DJANGO_WEBSERVER_DB_ENGINE={{ YOUR DB ENGINE }}
DJANGO_WEBSERVER_DB_NAME={{ YOUR DB NAME }}
DJANGO_WEBSERVER_DB_USER={{ YOUR DB USER }}
DJANGO_WEBSERVER_DB_PASSWORD={{ YOUR DB PASSWORD }} // NEVER POST THIS IN PUBLIC
DJANGO_WEBSERVER_DB_HOST={{ YOUR DB HOST }}
DJANGO_WEBSERVER_DB_PORT={{ YOUR DB PORT }}

AWS_REGION={{ YOUR AWS REGION ex. ap-northeast-2}}
AWS_STORAGE_BUCKET_NAME={{ YOUR AWS S3 BUCKET NAME }}
AWS_ACCESS_KEY_ID=YOUR AWS ACCESS KEY // NEVER POST THIS IN PUBLIC
AWS_SECRET_ACCESS_KEY=YOUR AWS SECRET ACCESS KEY // NEVER POST THIS IN PUBLIC
```

### Amazon Web Service (AWS)

```
AWS 계정과 CLI 환경의 crediential이 필요합니다. S3 bucket을 생성하고 public 설정을 해 주어야 합니다.

다른 환경에서 운영하기 위해서는, config/base.py 파일을 수정하기 바랍니다.
```

### Docker and docker-compose

```
https://docs.docker.com/compose/install/
```


### config/settings.py

개발 환경에 따라 config/settings.py을 다음과 같이 수정합니다.

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

## Run 

### on localhost

#### Installation

```bash
pip install pipenv

pipenv install --python $(which python3) --dev
```

#### Run

localhost 환경에서 작업하기 위해서는 3개의 터미널을 띄워야 합니다.

```bash
redis-server
```

```bash
pipenv shell

(pipenv shell) python manage.py rq-worker default
```

```bash
pipenv shell

(pipenv shell) python manage.py runserver 
```

### on docker

#### 올릴 때

```bash
sudo docker-compose up --build -d
```

#### 내릴 때

```bash
sudo docker-compose down
```
