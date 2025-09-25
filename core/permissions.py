from django.views import View
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsAdminOrReadOnly(BasePermission):
    """
    Permission class to restrict access based on user roles and HTTP methods.

    This permission class allows full access to users with staff status and
    read-only access (safe methods) to other users.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False


class SensorTokenAuthPermission(BasePermission):

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user
