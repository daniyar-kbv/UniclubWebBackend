from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return bool(
                hasattr(request.user, "club")
                and request.user.is_active
                and request.user.is_authenticated
            )

        return False
