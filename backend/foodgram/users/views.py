from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import FollowFilter
from .models import Follow, User
from .serializers import UserFollowSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """The class returns users of the online service."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["get", "post", "delete"]

    # @action(
    #     methods=["get"],
    #     detail=False,
    #     permission_classes=(IsAuthenticated,),
    #     url_path="me",
    # )
    # def me(self, request):
    #     """The function returns information about the current user."""
    #     serializer = UserSerializer(request.user)
    #     return Response(serializer.data)

    @action(
        methods=["get", "delete"],
        detail=True,
        permission_classes=(IsAuthenticated,),
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
            subscriptions = User.objects.filter(following__user=request.user)
            serializer = UserFollowSerializer(subscriptions)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            instance = Follow.objects.filter(
                following=blogger,
                user=request.user
            )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     methods=["get"],
    #     detail=False,
    #     permission_classes=(IsAuthenticated,),
    #     url_path="subscriptions"
    # )
    # def subscriptions(self, request):
    #     """The function returns all subscriptions."""
    #     subscriptions = request.user.follower.all()
    #     serializer = UserSerializer(subscriptions)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ModelViewSet):
    """The class returns a list of all subscribers and
    creates a subscription."""
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FollowFilter
    http_method_names = ["get"]

    def get_queryset(self):
        """The function returns a queryset containing all subscribers
        of the current user."""
        return User.objects.filter(following__user=self.request.user)
