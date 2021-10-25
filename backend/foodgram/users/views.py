from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import User
from.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """The class returns users of the online service."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
