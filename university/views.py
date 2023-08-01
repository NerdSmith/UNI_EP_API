from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator
from djoser.permissions import CurrentUserOrAdmin
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from university.models import Curator, Student, EduDirection, AcademicDiscipline, Group
from university.permissions import IsCurator, ReadOnly
from university.serializers import CuratorSerializer, StudentSerializer, EduDirectionSerializer, \
    AcademicDisciplineSerializer, GroupSerializer


class CuratorViewSet(ModelViewSet):
    serializer_class = CuratorSerializer
    queryset = Curator.objects.all()
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD
    permission_classes = [IsAdminUser, ]

    def permission_denied(self, request, **kwargs):
        if all((
                settings.HIDE_USERS,
                request.user.is_authenticated,
                self.action in ["update", "partial_update", "list", "retrieve"]
        )):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff and user.get_role() == "curator":
            queryset = queryset.filter(pk=user.curator.pk)
        return queryset

    def get_permissions(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy", "list"):
            self.permission_classes = [CurrentUserOrAdmin, ]
        return super().get_permissions()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD
    permission_classes = [IsAdminUser | IsCurator]

    def permission_denied(self, request, **kwargs):
        if all((
            settings.HIDE_USERS,
            request.user.is_authenticated,
            self.action in ["update", "partial_update", "list", "retrieve"]
        )):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action in ("retrieve", "update", "partial_update", "destroy", "list"):
            self.permission_classes = [CurrentUserOrAdmin | IsCurator]
        return super().get_permissions()


class EduDirectionViewSet(ModelViewSet):
    queryset = EduDirection.objects.all()
    serializer_class = EduDirectionSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class AcademicDisciplineViewSet(ModelViewSet):
    queryset = AcademicDiscipline.objects.all()
    serializer_class = AcademicDisciplineSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser | IsCurator | ReadOnly]
