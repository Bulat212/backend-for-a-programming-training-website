from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    Разрешает доступ только администратору или владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешить доступ, если пользователь администратор
        if request.user.is_staff:
            return True
        # Разрешить доступ, если пользователь является владельцем объекта
        return obj.user == request.user