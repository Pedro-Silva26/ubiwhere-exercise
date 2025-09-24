from django.views import View
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False
