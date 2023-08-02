from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from university.models import Curator, AcademicDiscipline, EduDirection, Group


class ReportCuratorSerializer(ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    patronymic = serializers.CharField(source='user.patronymic')

    class Meta:
        model = Curator
        fields = ('first_name', 'last_name', 'patronymic')


class ReportAcademicDisciplineSerializer(ModelSerializer):
    class Meta:
        model = AcademicDiscipline
        fields = ('title',)


class ReportEduDirectionDisciplineSerializer(ModelSerializer):
    disciplines = ReportAcademicDisciplineSerializer(many=True)
    curator = ReportCuratorSerializer()

    class Meta:
        model = EduDirection
        fields = ('title', 'disciplines', 'curator')


class ReportStudentSerializer(ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    patronymic = serializers.CharField(source='user.patronymic')
    gender = serializers.CharField(source='user.gender')

    class Meta:
        model = Curator
        fields = ('first_name', 'last_name', 'patronymic', 'gender')


class ReportGroupSerializer(ModelSerializer):
    males_count = serializers.SerializerMethodField('get_males_count')
    females_count = serializers.SerializerMethodField('get_females_count')
    free_place = serializers.SerializerMethodField('get_free_place')

    students = ReportStudentSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            'course_number',
            'group_number',
            'education_level',
            'males_count',
            'females_count',
            'free_place',
            'students'
        )

    def get_males_count(self, obj):
        return obj.get_males_count()

    def get_females_count(self, obj):
        return obj.get_females_count()

    def get_free_place(self, obj):
        return Group.STUDENT_MAX_COUNT - obj.get_current_students()


class ReportEduDirectionGroupSerializer(ModelSerializer):
    groups = ReportGroupSerializer(many=True)

    class Meta:
        model = EduDirection
        fields = ('title', 'groups',)