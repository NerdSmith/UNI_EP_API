from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from university.models import User, Curator


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
        fields = ('username',
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
        fields = ('user', )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = MyUserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        curator = Curator.objects.create(user=user)
        return curator
