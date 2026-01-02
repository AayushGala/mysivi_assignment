from rest_framework import permissions

class IsManagerOrReadOnlyAssigned(permissions.BasePermission):
    """
    Manager: CRUD on tasks they created.
    Reportee: Read assigned tasks, Update status only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'MANAGER':
            # Manager can only access tasks they created
            return obj.created_by == request.user
        
        elif request.user.role == 'REPORTEE':
            # Reportee can only access tasks assigned to them
            if obj.assigned_to != request.user:
                return False
            
            # Allow Read
            if request.method in permissions.SAFE_METHODS:
                return True
            
            # Allow Update (PUT/PATCH), validation of fields happens in Serializer/View
            if request.method in ['PUT', 'PATCH']:
                return True
                
        return False
