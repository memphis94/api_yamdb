from rest_framework import permissions


class GenresTitlesPermission(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return (
            request.method in permissions.SAFE_METHODS
            or is_admin
        )

class ReviewCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator')
                and request.user.is_authenticated)