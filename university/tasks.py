import os
from collections import OrderedDict
from typing import Tuple

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import xlsxwriter

from celery import shared_task
from django.conf import settings

from university.models import EduDirection
from university.report_serializers import ReportEduDirectionDisciplineSerializer, ReportEduDirectionGroupSerializer


def prepare_headlines_wr(main_title, worksheet, data) -> None:
    prepare_headlines(main_title, worksheet, data)


def prepare_headlines(main_title, worksheet, data, col=0, row=0) -> Tuple[int, int]:
    if data:
        for col_obj in data[0]:
            curr_obj = data[0][col_obj]
            if not isinstance(curr_obj, (OrderedDict, list, dict)):
                worksheet.write(row, col, f'{main_title}.{col_obj}')
                col += 1
            elif isinstance(curr_obj, (list,)):
                if not curr_obj:
                    worksheet.write(row, col, f'{col_obj}')
                    col += 1
                else:
                    col, row = prepare_headlines(col_obj, worksheet, curr_obj, col, row)
            elif isinstance(curr_obj, (OrderedDict, dict,)):
                for wr_key in data[0][col_obj].keys():
                    worksheet.write(row, col, f'{col_obj}.{wr_key}')
                    col += 1

    return col, row


def fill_data_wr(worksheet, data):
    fill_data(worksheet, data)


def fill_data(worksheet, data, col_=0, row_=1, need_wrap=False) -> Tuple[int, int]:
    rem_row = row_
    col = col_

    for obj in data:
        row = rem_row
        col = col_
        for col_obj in obj:
            curr_obj = obj[col_obj]
            if not isinstance(curr_obj, (OrderedDict, list, dict)):
                worksheet.write(row, col, f'{curr_obj}')
                col += 1
            elif isinstance(curr_obj, (list,)):
                col, rem_row = fill_data(worksheet, curr_obj, col, row, need_wrap=True)
            elif isinstance(curr_obj, (OrderedDict, dict,)):
                for wr_val in obj[col_obj].values():
                    worksheet.write(row, col, f'{wr_val}')
                    col += 1
        if need_wrap:
            rem_row += 1
    return col, rem_row


def generate_worksheet(workbook, name, main_title, queryset, serializer) -> None:
    worksheet = workbook.add_worksheet(name)
    serializer = serializer(queryset, many=True)

    prepare_headlines_wr(main_title, worksheet, serializer.data)
    fill_data(worksheet, serializer.data)


@shared_task()
def generate_report():
    filename = 'report.xlsx'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    workbook = xlsxwriter.Workbook(filepath)

    directions = EduDirection.objects.all()

    generate_worksheet(
        workbook,
        "DirectionsDisciplines",
        "direction",
        directions,
        ReportEduDirectionDisciplineSerializer
    )
    generate_worksheet(
        workbook,
        "GroupStudents",
        "direction",
        directions,
        ReportEduDirectionGroupSerializer
    )

    workbook.close()
    return filename


if __name__ == '__main__':
    generate_report()
