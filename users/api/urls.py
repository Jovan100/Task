from rest_framework import routers
from users.api.views import  UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
