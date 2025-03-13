from rest_framework.permissions import BasePermission
from core.models import RoleChoices
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != RoleChoices.ADMIN:
            raise PermissionDenied(
                'Only admin is allowed to access this route')
        return True


class CanCreateTodo(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
        print(request.user)
        if request.user.is_banned:
            return False
            # raise PermissionDenied(
            #     'You are no longer allowed to create a Todo')
        return True
