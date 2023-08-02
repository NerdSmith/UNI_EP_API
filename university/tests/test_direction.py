import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_edudir_by_admin(admin_client, edudir_payload):
    url = reverse('edudirections-list')
    response = admin_client.post(
        url,
        data=json.dumps(edudir_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED

    id = response.data.get('id')

    url = reverse('edudirections-list')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'edudirections-detail',
        kwargs={'pk': id}
    )
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'edudirections-detail',
        kwargs={'pk': id}
    )
    dir_put_payload = {'title': "newTitle"}
    response = admin_client.put(
        url,
        data=json.dumps(dir_put_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'edudirections-detail',
        kwargs={'pk': id}
    )
    dir_patch_payload = {'title': "newTitle"}
    response = admin_client.patch(
        url,
        data=json.dumps(dir_patch_payload),
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK

    url = reverse(
        'edudirections-detail',
        kwargs={'pk': id}
    )
    response = admin_client.delete(
        url
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
