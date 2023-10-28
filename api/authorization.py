from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        # Seuls les managers ont accès, les autres ont seulement la permission de lecture
        return request.user.role == 'Manager' or request.method in permissions.SAFE_METHODS


class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Etudiant' or request.method in permissions.SAFE_METHODS
