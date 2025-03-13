from rest_framework.permissions import BasePermission
from core.models import RoleChoices
from rest_framework.exceptions import PermissionDenied


class IsAdmin(BasePermission):
    '''
    Added to routes accessible by admin only
    '''

    def has_permission(self, request, view):
        if request.user.role != RoleChoices.ADMIN:
            raise PermissionDenied(
                'Only admin is allowed to access this route')
        return True


class CanCreateTodo(BasePermission):
    '''
    Check if logged-in user has the permission to create todos i.e. they are not banned
    '''

    def has_permission(self, request, view):
        if request.method not in ['POST', 'PUT', 'PATCH']:
            return True
        print(request.user)
        if request.user.is_banned:
            raise PermissionDenied(
                'You are no longer allowed to create a Todo')
        return True
