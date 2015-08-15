from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyPermissions(BasePermission):
    """ Read Only Permissions """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS and request.user and request.user.is_authenticated()
        )


class SuperUserOnlyPermissions(BasePermission):
    """ Super User  """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False