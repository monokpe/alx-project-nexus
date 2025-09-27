# products/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects,
    but allow anyone to view them.
    """

    def has_permission(self, request, view):
        # Allow all GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Deny write permissions for non-authenticated users.
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow write permissions only if the user is a staff member.
        return request.user.is_staff