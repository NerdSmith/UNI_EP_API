import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_student_by_unauthorized(client, student_payload):
    url = reverse('students-list')
    response = client.post(
        url,
        student_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse('students-list')
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'students-detail',
        kwargs={'id': 0}
    )
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'students-detail',
        kwargs={'id': 0}
    )
    student_payload['user']["first_name"] = "Oleg"
    response = client.put(
        url,
        data=student_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'students-detail',
        kwargs={'id': 0}
    )
    student_payload['user']["first_name"] = "Oleg"
    response = client.patch(
        url,
        data=student_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'students-detail',
        kwargs={'id': 0}
    )
    response = client.delete(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_student_by_admin(admin_client, student_payload):
    url = reverse('students-list')
    response = admin_client.post(
        url,
        data=student_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    id = response.data.get('pk')

    url = reverse('students-list')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_put_payload = {}
    student_put_payload['user'] = {}
    student_put_payload['user']["first_name"] = "Oleg"
    response = admin_client.put(
        url,
        data=student_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_patch_payload = {}
    student_patch_payload['user'] = {}
    student_patch_payload['user']["first_name"] = "Oleg"
    response = admin_client.patch(
        url,
        data=student_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = admin_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_student_by_curator(curator_client, student_payload):
    url = reverse('students-list')
    response = curator_client.post(
        url,
        data=json.dumps(student_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    id = response.data.get('pk')

    url = reverse('students-list')
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_put_payload = {}
    student_put_payload['user'] = {}
    student_put_payload['user']["first_name"] = "Oleg"
    response = curator_client.put(
        url,
        data=json.dumps(student_put_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_patch_payload = {}
    student_patch_payload['user'] = {}
    student_patch_payload['user']["first_name"] = "Oleg"
    response = curator_client.patch(
        url,
        data=json.dumps(student_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = curator_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_student_by_student(student_client, student_payload):
    url = reverse('students-list')
    response = student_client.post(
        url,
        data=json.dumps(student_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    id = response.data.get('pk')

    url = reverse('students-list')
    response = student_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = student_client.get(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_put_payload = {}
    student_put_payload['user'] = {}
    student_put_payload['user']["first_name"] = "Oleg"
    response = student_client.put(
        url,
        data=json.dumps(student_put_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    student_patch_payload = {}
    student_patch_payload['user'] = {}
    student_patch_payload['user']["first_name"] = "Oleg"
    response = student_client.patch(
        url,
        data=json.dumps(student_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = student_client.delete(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_student_self(student_client, student_user):
    id = student_user.pk

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    curator_put_payload = {"user": {
        "first_name": "Oleg"
    }}
    response = student_client.put(
        url,
        data=json.dumps(curator_put_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    curator_patch_payload = {"user": {
        "first_name": "Oleg"
    }}
    response = student_client.patch(
        url,
        data=json.dumps(curator_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'students-detail',
        kwargs={'id': id}
    )
    response = student_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
