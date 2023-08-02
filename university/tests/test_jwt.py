import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_jwt_unauthorized(client):
    url = reverse('jwt-create')
    response = client.post(
        url,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def check_token(client, user_data) -> None:
    url = reverse('jwt-create')
    response = client.post(
        url,
        data=user_data,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    access = response.data['access']
    refresh = response.data['refresh']
    url = reverse('jwt-verify')
    response = client.post(
        url,
        data={
            "token": access
        },
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse('jwt-refresh')
    response = client.post(
        url,
        data={
            "refresh": refresh
        },
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_jwt_admin(client, admin_user):
    user_data = {"password": "password", "username": "admin"}
    check_token(client, user_data)


@pytest.mark.django_db
def test_jwt_curator(client, curator_user):
    user_data = {"password": "1029qpwo", "username": "curator"}
    check_token(client, user_data)


@pytest.mark.django_db
def test_jwt_student(client, student_user):
    user_data = {"password": "1029qpwo", "username": "student"}
    check_token(client, user_data)
