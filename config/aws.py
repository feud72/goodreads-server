# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "54.180.97.10",
    "hackathon.hopto.org",
    "127.0.0.1",
]
COOKIE_DOMAIN = "hackathon.hopto.org"

RQ_QUEUES = {
    "default": {"HOST": "redis", "PORT": 6379, "DB": 0, "DEFAULT_TIMEOUT": 360,},
}
