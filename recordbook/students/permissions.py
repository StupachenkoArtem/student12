from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return bool(obj.user == request.user or request.user.is_staff)
        elif request.method == 'DELETE':
            return bool(request.user.is_staff)
        else:
            return False
