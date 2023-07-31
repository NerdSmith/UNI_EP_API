from django.urls import path, include
from rest_framework import routers

from university.views import CuratorViewSet, StudentViewSet, EduDirectionViewSet

auth_router = routers.SimpleRouter()
auth_router.register('auth/users/curators', CuratorViewSet)
auth_router.register('auth/users/students', StudentViewSet)

edu_router = routers.SimpleRouter()
edu_router.register('edudirection', EduDirectionViewSet)

urlpatterns = [

]

urlpatterns += auth_router.urls
urlpatterns += edu_router.urls
