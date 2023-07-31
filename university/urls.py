from django.urls import path, include
from rest_framework import routers

from university.views import CuratorViewSet, StudentViewSet, EduDirectionViewSet, AcademicDisciplineViewSet, \
    GroupViewSet

auth_router = routers.SimpleRouter()
auth_router.register('auth/users/curators', CuratorViewSet)
auth_router.register('auth/users/students', StudentViewSet)

edu_router = routers.SimpleRouter()
edu_router.register('edudirections', EduDirectionViewSet)
edu_router.register('disciplines', AcademicDisciplineViewSet)
edu_router.register('groups', GroupViewSet)

urlpatterns = [

]

urlpatterns += auth_router.urls
urlpatterns += edu_router.urls
