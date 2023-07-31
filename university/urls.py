from django.urls import path, include
from rest_framework import routers

from university.views import CuratorViewSet

router = routers.SimpleRouter()
router.register('auth/users/curators', CuratorViewSet)

urlpatterns = [

]

urlpatterns += router.urls
