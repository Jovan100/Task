from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from users.models import User
from users.api.serializers import UserSerializer
from users.api.permissions import IsAdminOrOwner
from django.shortcuts import get_object_or_404

class GenericModelViewSet(ModelViewSet):
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

class UserViewSet(GenericModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'list': [IsAdminUser],
        'retrieve': [IsAdminOrOwner],
        'update': [IsAdminOrOwner],
        'partial_update': [IsAdminOrOwner],
        'destroy': [IsAdminOrOwner]
    }
