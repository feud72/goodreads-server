## API Documentation

### [API Link](https://github.com/feud72/goodreads-server/blob/master/api.md)

## Prerequisite

- 카카오 개발자 페이지, 도서관 정보나루, AWS 에서 KEY를 발급받아야 합니다.

- docker, docker-compose 설치가 필요합니다.

  - localhost에서 돌리는 경우 redis 설치가 필요합니다.

### 카카오 개발자 페이지

https://developers.kakao.com

#### 앱 생성

https://developers.kakao.com/apps/new

#### REST API KEY 발급

```
https://developers.kakao.com/apps/{{ YOUR APP }}/settings/general
```

키를 발급받은 후 .env > KAKAO_ID 에 저장합니다.


#### Set Login Redirect URI

```
https://developers.kakao.com/apps/{{ YOUR APP }}/settings/user
```

Login Redirect URI를 웹페이지의 주소와 같도록 등록합니다.


### 도서관 정보나루

#### API KEY 발급

https://www.data4library.kr/apiUtilization

키를 발급받은 후 .env > LIB_KEY에 저장합니다.

### Amazon Web Service (AWS)

AWS 계정과 CLI 환경의 credential이 필요합니다. 

S3 bucket을 생성하고 public 설정을 해 주어야 합니다.

다른 환경에서 운영하기 위해서는, config/base.py 파일을 수정하기 바랍니다.

### .env 작성

프로젝트 디렉토리에 .env 를 생성하여 다음과 같이 작성합니다.

Caution : docker-compose 환경의 .env 파일은 쌍따옴표(")가 들어가면 안됩니다.

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

### config/settings.py

개발 환경에 따라 config/settings.py을 다음과 같이 수정합니다.

필요에 따라 config/settings.py 또는 config/dev.py 등에 ALLOWED_HOSTS 세팅을 추가합니다.

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

### Docker and docker-compose

https://docs.docker.com/compose/install/

## Run 

### on localhost

#### Installation

```bash
pip install pipenv

pipenv install --python $(which python3) --dev

pipenv shell

(pipenv shell) python manage.py makemigrations

(pipenv shell) python manage.py migrate
```

#### Run

localhost 환경에서 작업하기 위해서는 3개의 터미널을 띄워야 합니다.

##### Redis

https://redis.io/download

```bash
redis-server
```

##### rq(Redis queue)

```bash
pipenv shell

(pipenv shell) python manage.py rq-worker default
```

##### django

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
