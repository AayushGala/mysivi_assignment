from rest_framework import viewsets, filters 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .permissions import IsManagerOrReadOnlyAssigned

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnlyAssigned]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'status']
    ordering_fields = ['created_at', 'status']
    
    # We will set throttle_scope dynamically, so we must include ScopedRateThrottle
    # But it is already in DEFAULT_THROTTLE_CLASSES.
    
    def get_throttles(self):
        if self.action == 'create':
            self.throttle_scope = 'task-create'
        elif self.action == 'list':
            self.throttle_scope = 'task-list'
        else:
            self.throttle_scope = None # Fallback to UserRateThrottle defaults
        return super().get_throttles()

    def get_queryset(self):
        user = self.request.user
        base_qs = Task.objects.filter(is_deleted=False)
        if user.role == 'MANAGER':
            return base_qs.filter(created_by=user)
        elif user.role == 'REPORTEE':
            return base_qs.filter(assigned_to=user)
        return Task.objects.none()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
    
    def perform_create(self, serializer):
        if self.request.user.role != 'MANAGER':
            raise PermissionDenied("Only Managers can create tasks.")
        serializer.save(created_by=self.request.user)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    # Just to list categories if needed
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
