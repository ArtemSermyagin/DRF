from rest_framework import permissions

from users.models import User


class UserRightPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.filter(pk=view.kwargs.get('pk'))
        if not user:
            return False

        if user[0] == request.user:
            return True
        return False


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
