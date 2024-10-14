from rest_framework import permissions

class IsAuthenticatedAndUser(permissions.BasePermission):
    """
    Permissão que permite acesso apenas a usuários autenticados.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated