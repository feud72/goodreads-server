from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .serializers import RegistrationSerializer, LoginSerializer

from utils.jwt import encode_jwt


class LoginView(GenericAPIView):
    """
    로그인
    """

    serializer_class = LoginSerializer

    def post(self, request):
        """
    로그인

    ## Specification
    - **Method** :  POST
    - **URL** : /api/v1/accounts/login/
    - **Content-Type** : application/json; charset=utf-8
    - **Parameters**

    | 필드명 | 타입 | 필수여부 | 설명 |
    | ---- | ---- | -------- | ----------- |
    | email | string | Required | 이메일 |
    | password | string | Required | 비밀번호 |

        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = get_user_model().objects.get(email=email)
            if user is not None:
                token = encode_jwt("pk", user.pk)
                return Response(
                    status=status.HTTP_200_OK,
                    data={"message": "success", "token": token, "id": user.pk},
                )
            else:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"detail": "Unauthorized."},
                )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class SignupView(GenericAPIView):
    """
    회원가입
    """

    serializer_class = RegistrationSerializer

    def post(self, request):
        """
    회원가입

    ## Specification
    - **Method** :  POST
    - **URL** : /api/v1/accounts/signup/
    - **Content-Type** : application/json; charset=utf-8
    - **Parameters**

    | 필드명 | 타입 | 필수여부 | 설명 |
    | ---- | ---- | -------- | ----------- |
    | email | string | Required | 이메일 |
    | password1 | string | Required | 비밀번호 |
    | password2 | string | Required | 비밀번호 |

    - **Response**

    | 성공 (201 Created) |
    | ---- |

    | 필드명 | 타입 | 필수여부 | 설명 |
    | ---- | ---- | -------- | ----------- |
    | message | string | | 성공시 success |
    | email | string | | 유저의 email |
    | current_bookshelf | object | | 회원 가입시 책장이 자동으로 생성됩니다. |

    | 실패 (400 Bad Request) |
    | ---- |

    | 필드명 | 타입 | 필수여부 | 설명 |
    | ---- | ---- | -------- | ----------- |
    | detail | string | | 오류가 발생한 필드와 상세 내역을 리스트 형식으로 반환|


    예제
    ```json
    {
    "message": "success",
    "email": "user@example.com",
    "current_bookshelf": {
        "id": 21,
        "created_at": "2020-02-06",
        "name": "내 책장",
        "gender": "N",
        "age": null,
        "owner": 17
        }
    }
    ```

    실패 예제
    ```json
    {
    "detail": {
        "email": [
            "Email is already taken."
        ],
        "password1": [
            "This password is too short. It must contain at least 8 characters."
        ]
    }
    }
    ```
        """
        serializer = self.get_serializer(data=request.data)
        message = {}
        if serializer.is_valid():
            user = serializer.save()
            message["message"] = "success"
            message["email"] = user.email
            return Response(status=status.HTTP_201_CREATED, data=message)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data={"detail": serializer.errors}
            )
