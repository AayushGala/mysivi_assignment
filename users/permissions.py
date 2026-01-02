from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Allows access only to Managers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'MANAGER')

class IsReportee(permissions.BasePermission):
    """
    Allows access only to Reportees.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'REPORTEE')
