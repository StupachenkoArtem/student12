import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Student
        fields = ('last_name', 'first_name', 'middle_name', 'group', 'slug', 'photo', 'user')


class StudentModel:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


# class StudentSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)


def encode():
    model = StudentModel('Elon', 'Musk')
    model_sr = StudentSerializer(model)
    print(model_sr.data, type(model_sr.data), sep='\n')
    json = JSONRenderer().render(model_sr.data)
    print(json, type(json), sep='\n')


def decode():
    stream = io.BytesIO(b'{"first_name":"Elon","last_name":"Musk"}')
    data = JSONParser().parse(stream)
    serializer = StudentSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)


class StudentDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    group_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_group_name(self, obj):
        print(obj)
        return f'{obj.group.course}-{obj.group.name}'

    def get_username(self, obj):
        print(obj)
        return obj.user.get_username()
