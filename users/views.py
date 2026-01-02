from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.throttling import ScopedRateThrottle
from .serializers import ManagerSignupSerializer, CreateReporteeSerializer, UserSerializer
from .permissions import IsManager

class ManagerSignupView(generics.CreateAPIView):
    serializer_class = ManagerSignupSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'auth' # Applying scoped throttling

class CustomLoginView(ObtainAuthToken):
    throttle_scope = 'auth' # Applying scoped throttling
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': user.role,
            'username': user.username
        })

class CreateReporteeView(generics.CreateAPIView):
    serializer_class = CreateReporteeSerializer
    permission_classes = [IsAuthenticated, IsManager]
    # Uses default UserRateThrottle unless specified otherwise

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ManageReporteesView(generics.ListAPIView):
     # Optional: Helper to see my reportees
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]

    def get_queryset(self):
        return self.request.user.reportees.all()
