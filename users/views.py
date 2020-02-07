from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

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
