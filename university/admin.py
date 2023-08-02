from django.contrib import admin
from django.contrib.auth.models import Group

from university.models import User, EduDirection, AcademicDiscipline, Group as MyGroup

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(EduDirection)
admin.site.register(AcademicDiscipline)
admin.site.register(MyGroup)
