# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

RQ_QUEUES = {
    "default": {"HOST": "127.0.0.1", "PORT": 6379, "DB": 0, "DEFAULT_TIMEOUT": 360,},
}

COOKIE_DOMAIN = "127.0.0.1"
