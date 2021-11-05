from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet
router = DefaultRouter()
router.register("users", UserViewSet, basename="User")

urlpatterns = [
    # path("", include("djoser.urls")),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
# router.register(
#     "users/subscriptions",
#     FollowViewSet,
#     basename="Follows"
# )
