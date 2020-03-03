DEBUG = False
ALLOWED_HOSTS = [
    "ec2-54-180-97-10.ap-northeast-2.compute.amazonaws.com",
    "54.180.97.10",
    "hackathon.hopto.org",
]
COOKIE_DOMAIN = "hackathon.hopto.org"

RQ_QUEUES = {
    "default": {"HOST": "redis", "PORT": 6379, "DB": 0, "DEFAULT_TIMEOUT": 360,},
}
