from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, UserViewSet
router = DefaultRouter()
router.register("users", UserViewSet, basename="User")

urlpatterns = [
    path(
        "users/subscriptions/",
        FollowViewSet.as_view(({'get': 'list'})),
        name="Subscriptions"
    ),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    # path("users/", include([
    #     path(
    #         "subscriptions/",
    #         FollowViewSet.as_view(({'get': 'list'})),
    #         name="Subscriptions"
    #     ),
    #     path("auth/", include("djoser.urls.authtoken")),
    # ])),
]
