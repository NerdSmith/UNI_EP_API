from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from university.models import Curator, Student, EduDirection, AcademicDiscipline, Group
from university.permissions import IsCurator, ReadOnly, CurrentUserOrAdmin
from university.serializers import CuratorCreateSerializer, StudentCreateSerializer, EduDirectionSerializer, \
    AcademicDisciplineSerializer, GroupSerializer, CuratorSerializer, StudentSerializer
from university.tasks import generate_report


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

    def get_serializer_class(self):
        if self.action == "create":
            return CuratorCreateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        return super().update(request, partial=True)

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

    def get_serializer_class(self):
        if self.action == "create":
            return StudentCreateSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        if request.user.get_role() == "student":
            request.data = request.data.pop("user", {})
        return super().update(request, partial=True)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.student.pk)
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


class ReportView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, *args, **kwargs):
        task = generate_report.delay()
        response = {"task_id": task.task_id}
        return Response(response, status=status.HTTP_202_ACCEPTED)


class ReportStatusView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, task_id, format=None):
        task = generate_report.AsyncResult(task_id)
        if task.state == 'PENDING':
            return Response({'status': 'Pending'}, status=status.HTTP_202_ACCEPTED)
        elif task.state == 'FAILURE':
            return Response({'status': 'Failure'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif task.state == 'SUCCESS':
            report_filename = task.result
            from django.conf import settings
            media_url = request.build_absolute_uri(settings.MEDIA_URL)
            return Response(
                {
                    'status': 'Success',
                    'url': media_url + report_filename
                }, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
