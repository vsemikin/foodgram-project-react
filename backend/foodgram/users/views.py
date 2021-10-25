from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """The class returns users of the online service."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
