import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_group_by_curator(curator_client, group_payload):
    url = reverse('groups-list')
    response = curator_client.post(
        url,
        data=json.dumps(group_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    id = response.data.get('id')

    url = reverse('groups-list')
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'groups-detail',
        kwargs={'pk': id}
    )
    response = curator_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'groups-detail',
        kwargs={'pk': id}
    )
    group_payload.update({"course_number": 2})
    response = curator_client.put(
        url,
        data=json.dumps(group_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'groups-detail',
        kwargs={'pk': id}
    )
    group_patch_payload = {'title': "newTitle"}
    response = curator_client.patch(
        url,
        data=json.dumps(group_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'groups-detail',
        kwargs={'pk': id}
    )
    response = curator_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_student_group_assign(curator_client, group, student_user):
    url = reverse(
        'students-detail',
        kwargs={'id': student_user.pk}
    )
    student_patch_payload = {"group": group.pk}
    response = curator_client.patch(
        url,
        data=json.dumps(student_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK
