import datetime

from django.conf import settings

import jwt


def encode_jwt(keyword, value):
    encoded_jwt = jwt.encode(
        {
            keyword: value,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def decode_jwt(data):
    decoded_jwt = jwt.decode(data, settings.SECRET_KEY, algorithm="RS256")
    return decoded_jwt
