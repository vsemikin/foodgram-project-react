from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """The class returns users of the online service."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "delete"]

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
    )
    def me(self, request):
        """."""
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get", "delete"],
        url_path="subscribe"
    )
    def subscribe(self, request, pk=None):
        """Function to add or remove a subscribe."""
        blogger = self.get_object()
        if request.method == "GET":
            instance = Follow.objects.create(
                following=blogger,
                user=request.user
            )
            serializer = FollowSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            instance = Follow.objects.filter(
                following=blogger,
                user=request.user
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ModelViewSet):
    """The class returns a list of all subscribers and
    creates a subscription."""
    serializer_class = FollowSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        """The function returns a queryset containing all subscribers
        of the current user."""
        return self.request.user.follower.all()
