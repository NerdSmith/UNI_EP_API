from django.urls import path
from rest_framework import routers

from university.views import CuratorViewSet, StudentViewSet, EduDirectionViewSet, AcademicDisciplineViewSet, \
    GroupViewSet, ReportView, ReportStatusView

auth_router = routers.SimpleRouter()
auth_router.register('auth/users/curators', CuratorViewSet, basename="curators")
auth_router.register('auth/users/students', StudentViewSet, basename="students")

edu_router = routers.SimpleRouter()
edu_router.register('edudirections', EduDirectionViewSet)
edu_router.register('disciplines', AcademicDisciplineViewSet)
edu_router.register('groups', GroupViewSet)

urlpatterns = [
    path(r'report/<str:task_id>', ReportStatusView.as_view()),
    path(r'report', ReportView.as_view()),
]

urlpatterns += auth_router.urls
urlpatterns += edu_router.urls
