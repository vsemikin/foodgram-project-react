from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        """The function creates a permission at the object level that prohibits editing
        an objectthat is not its own."""
        return (
            (request.method in permissions.SAFE_METHODS)
            or (obj.author == request.user)
        )
