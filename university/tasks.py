import os

import xlsxwriter

from celery import shared_task
from django.conf import settings

from university.models import EduDirection, Group


def prepare_directions_disciplines_headline(worksheet):
    worksheet.write(0, 0, "Directions")
    worksheet.write(0, 1, "Disciplines")
    worksheet.write(0, 2, "Curators")


def prepare_group_students_headline(worksheet):
    worksheet.write(0, 0, "Groups")
    worksheet.write(0, 1, "Students")
    worksheet.write(0, 2, "Males")
    worksheet.write(0, 3, "Females")
    worksheet.write(0, 4, "FreeSpace")


def generate_directions_disciplines(workbook):
    dir_disc_worksheet = workbook.add_worksheet("DirectionsDisciplines")

    prepare_directions_disciplines_headline(dir_disc_worksheet)

    directions = EduDirection.objects.all()

    row = 1
    col = 0

    for direction in directions:
        dir_disc_worksheet.write(row, col, str(direction))
        dir_disc_worksheet.write(row, col + 2, str(direction.curator)) \
            if direction.curator else dir_disc_worksheet.write(row, col, None)

        for discipline in direction.disciplines.all():
            dir_disc_worksheet.write(row, col + 1, str(discipline))
            row += 1
        else:
            row += 1


def generate_group_students(workbook):
    group_students_worksheet = workbook.add_worksheet("GroupStudents")

    prepare_group_students_headline(group_students_worksheet)

    groups = Group.objects.all()

    row = 1
    col = 0

    for group in groups:
        group_students_worksheet.write(row, col, str(group))
        group_students_worksheet.write(row, col + 2, int(group.get_females_count()))
        group_students_worksheet.write(row, col + 3, int(group.get_males_count()))
        group_students_worksheet.write(row, col + 4, int(group.STUDENT_MAX_COUNT - group.get_current_students()))
        for student in group.students.all():
            group_students_worksheet.write(row, col + 1, str(student))
            row += 1
        else:
            row += 1


@shared_task()
def generate_report():
    filename = 'report.xlsx'
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    workbook = xlsxwriter.Workbook(filepath)
    generate_directions_disciplines(workbook)
    generate_group_students(workbook)
    workbook.close()
    return filename


if __name__ == '__main__':
    generate_report()

