from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from university.models import User, Curator, Student, Group, EduDirection, AcademicDiscipline


class MyUserSerializer(UserCreateSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    patronymic = serializers.CharField(max_length=20)
    email = serializers.CharField()
    role = serializers.SerializerMethodField('find_role', read_only=True, required=False)

    def find_role(self, obj) -> str:
        return obj.get_role()

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   patronymic=validated_data['patronymic'],
                                   email=validated_data['email']
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('pk',
                  'username',
                  'password',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'email',
                  'role',
                  )


class CuratorSerializer(ModelSerializer):
    user = MyUserSerializer(required=True)

    class Meta:
        model = Curator
        fields = ('pk', 'user', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = MyUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        curator = Curator.objects.create(user=user)
        return curator


class StudentSerializer(ModelSerializer):
    user = MyUserSerializer(required=True)

    class Meta:
        model = Student
        fields = ('pk', 'user', 'group')

    def validate_group(self, value):
        if value:
            target_group = Group.objects.get(pk=value.pk)
            if target_group and target_group.students.count() < Group.STUDENT_MAX_COUNT:
                return value
            else:
                raise serializers.ValidationError("Max students in group")
        raise serializers.ValidationError("Group field not set")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        group = validated_data['group']
        user_serializer = MyUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        student = Student.objects.create(user=user, group=group)
        return student


class EduDirectionSerializer(ModelSerializer):
    class Meta:
        model = EduDirection
        fields = '__all__'


class AcademicDisciplineSerializer(ModelSerializer):
    class Meta:
        model = AcademicDiscipline
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
