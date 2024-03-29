import pytest
from django.contrib.auth.hashers import make_password

from university.models import Curator, Student, EduDirection, Group


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def curator_payload():
    payload = {
        "user": {
            "username": "curator",
            "password": "1029qpwo",
            "first_name": "Curator",
            "last_name": "Curator",
            "patronymic": "Curator",
            "email": "curator@gmail.com"
        }
    }
    return payload


@pytest.fixture
def student_payload():
    payload = {
        "user": {
            "username": "student",
            "password": "1029qpwo",
            "first_name": "Student",
            "last_name": "Student",
            "patronymic": "Student",
            "email": "student@gmail.com"
        }
    }
    return payload


@pytest.fixture
def edudir_payload(curator_user):
    payload = {
        "title": "edudir",
        "curator": curator_user.pk
    }
    return payload


@pytest.fixture
def discipline_payload(edudir):
    payload = {
        "title": "discipline",
        "description": "discipline discipline discipline",
        "direction": edudir.pk
    }
    return payload


@pytest.fixture
def group_payload(edudir):
    payload = {
        "course_number": 1,
        "group_number": "1.1",
        "education_level": "b",
        "direction": edudir.pk
    }
    return payload


@pytest.fixture
def group(db, group_payload, edudir):
    group_payload["direction"] = edudir
    return Group.objects.create(**group_payload)


@pytest.fixture
def edudir(db, edudir_payload):
    edudir_payload["curator"] = Curator.objects.get(pk=edudir_payload["curator"])
    return EduDirection.objects.create(**edudir_payload)


@pytest.fixture
def curator_user(db, django_user_model, curator_payload):
    UserModel = django_user_model
    username = "curator"
    curator_payload["user"]["password"] = make_password(curator_payload.get("user").get("password"))
    try:
        curator = Curator.objects.get(user__username=username)
    except Curator.DoesNotExist:
        user = UserModel.objects.create(**curator_payload.get("user"))
        curator = Curator.objects.create(user=user)
    return curator


@pytest.fixture
def curator_client(api_client, curator_user):
    api_client.force_authenticate(curator_user.user)
    return api_client


@pytest.fixture
def student_user(django_user_model, student_payload):
    UserModel = django_user_model
    username = "student"
    student_payload["user"]["password"] = make_password(student_payload.get("user").get("password"))
    try:
        student = Student.objects.get(user__username=username)
    except Student.DoesNotExist:
        user = UserModel.objects.create(**student_payload.get("user"))
        student = Student.objects.create(user=user)
    return student


@pytest.fixture
def student_client(api_client, student_user):
    api_client.force_authenticate(student_user.user)
    return api_client
