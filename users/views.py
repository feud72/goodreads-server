from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, action
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf


class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):

        if self.action == "list":
            # permission_classes = [IsAuthenticated]
            permission_classes = [AllowAny]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset.all().order_by("id")
        return queryset

    @action(
        detail=False, methods=["GET", "PUT", "DELETE"],
    )
    @permission_classes([IsSelf])
    def me(self, request, *args, **kwargs):
        """
Get User's information

---

## Specification
- **Method** :  GET
- **URL** : /api/v1/users/me/
- **Content-Type** : application/json; charset=utf-8
- **Parameters**

Not required.
        """
        try:
            instance = get_user_model().objects.get(username=request.user)
            serializer = self.get_serializer(instance)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
