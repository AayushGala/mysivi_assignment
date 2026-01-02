from django.urls import path
from .views import ManagerSignupView, CustomLoginView, CreateReporteeView, ManageReporteesView

urlpatterns = [
    path('signup/manager/', ManagerSignupView.as_view(), name='manager-signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('create-reportee/', CreateReporteeView.as_view(), name='create-reportee'),
    path('reportees/', ManageReporteesView.as_view(), name='list-reportees'),
]
