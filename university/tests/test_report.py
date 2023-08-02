import json
import time

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from university.tasks import generate_report


@pytest.mark.django_db
def test_report_business(admin_client, edudir, student_user):
    res = generate_report()
    assert res == "report.xlsx"


@pytest.mark.django_db
def test_report_gen(admin_client, edudir, student_user):
    url = reverse('get-report')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.django_db
def test_report_status(admin_client, edudir, student_user):
    url = reverse('get-report')
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_202_ACCEPTED

    time.sleep(10)

    url = reverse(
        'get-report-status',
        kwargs={'task_id': response.data.pop("task_id", "")}
    )
    response = admin_client.get(
        url
    )
    assert response.status_code == status.HTTP_200_OK
