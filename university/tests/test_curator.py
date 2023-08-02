import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_curator_by_unauthorized(client, curator_payload):
    url = reverse('curators-list')
    response = client.post(
        url,
        curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse('curators-list')
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'curators-detail',
        kwargs={'id': 0}
    )
    response = client.get(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'curators-detail',
        kwargs={'id': 0}
    )
    curator_payload['user']["first_name"] = "Oleg"
    response = client.put(
        url,
        data=curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'curators-detail',
        kwargs={'id': 0}
    )
    curator_payload['user']["first_name"] = "Oleg"
    response = client.patch(
        url,
        data=curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    url = reverse(
        'curators-detail',
        kwargs={'id': 0}
    )
    response = client.delete(
        url
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_curator_by_admin(admin_client, curator_payload):
    url = reverse('curators-list')
    response = admin_client.post(
        url,
        data=curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    id = response.data.get('pk')

    url = reverse('curators-list')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_put_payload = {}
    curator_put_payload['user'] = {}
    curator_put_payload['user']["first_name"] = "Oleg"
    response = admin_client.put(
        url,
        data=curator_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_patch_payload = {}
    curator_patch_payload['user'] = {}
    curator_patch_payload['user']["first_name"] = "Oleg"
    response = admin_client.patch(
        url,
        data=curator_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = admin_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_curator_by_curator(curator_client, curator_payload):
    url = reverse('curators-list')
    response = curator_client.post(
        url,
        data=curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    id = response.data.get('pk')

    url = reverse('curators-list')
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_put_payload = {}
    curator_put_payload['user'] = {}
    curator_put_payload['user']["first_name"] = "Oleg"
    response = curator_client.put(
        url,
        data=curator_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_patch_payload = {}
    curator_patch_payload['user'] = {}
    curator_patch_payload['user']["first_name"] = "Oleg"
    response = curator_client.patch(
        url,
        data=curator_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = curator_client.delete(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_curator_by_student(student_client, curator_payload):
    url = reverse('curators-list')
    response = student_client.post(
        url,
        data=curator_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    id = response.data.get('pk')

    url = reverse('curators-list')
    response = student_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = student_client.get(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_put_payload = {}
    curator_put_payload['user'] = {}
    curator_put_payload['user']["first_name"] = "Oleg"
    response = student_client.put(
        url,
        data=curator_put_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_patch_payload = {}
    curator_patch_payload['user'] = {}
    curator_patch_payload['user']["first_name"] = "Oleg"
    response = student_client.patch(
        url,
        data=curator_patch_payload,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = student_client.delete(
        url
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_curator_self(curator_client, curator_user):
    id = curator_user.pk

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_put_payload = {"user": {
        "first_name": "Oleg"
    }}
    response = curator_client.put(
        url,
        data=json.dumps(curator_put_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    curator_patch_payload = {"user": {
        "first_name": "Oleg"
    }}
    response = curator_client.patch(
        url,
        data=json.dumps(curator_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'curators-detail',
        kwargs={'id': id}
    )
    response = curator_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
