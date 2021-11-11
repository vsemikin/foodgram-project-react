from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("", include("recipes.urls")),
                path("", include("users.urls")),
            ]
        ),
    ),
]
