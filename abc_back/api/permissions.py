from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_superuser)
