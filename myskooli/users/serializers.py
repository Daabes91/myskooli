import base64
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from ..system.serializers import SubcategorySerializer
from ..system.model import SubCategory

from .models import Student, Teacher, Reviews, Post, Reply, Favorite, Lessons, PackageLessons, AvailableTime

from django.contrib.auth import get_user_model, authenticate
from django.conf import settings

from rest_framework import serializers, exceptions

User = get_user_model()


class StudentSignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        label="Email Address"
    )
    username = serializers.CharField(
        required=True,
        label="username"
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )



    class Meta(object):
        model = Student
        fields = ['id', 'username', 'email', 'password', 'name', 'image', 'phoneNumber', 'role']
        read_only_fields = ['role']

    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(StudentSignUpSerializer, self).create(validated_data)


    def validate_username(self, value):
        if Student.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class TeacherSignUpSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        label="Email Address"
    )
    username = serializers.CharField(
        required=True,
        label="username"
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta(object):
        model = Teacher
        fields = ['id', 'username', 'email', 'password', 'name', 'resume', 'phoneNumber', 'role','image','subcategory'
                  ,'video','teacher_type', 'about', 'skypeId', 'me_as_teacher', 'teaching_description', 'experience', 'certificate', 'education', 'country']
        read_only_fields = ['role']

    def validate_email(self, value):
        if Teacher.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(TeacherSignUpSerializer, self).create(validated_data)


    def validate_username(self, value):
        if Teacher.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)

    password = serializers.CharField(max_length=128, write_only=True)

    class Meta(object):
        fields = ('username','password')
        model = User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class StudentSerializer(serializers.ModelSerializer):
     class Meta:
         model = Student
         fields = ['id', 'username', 'email', 'password', 'name', 'image', 'phoneNumber', 'role']
         read_only_fields = ['role']


class AvailableTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvailableTime
        fields = ('id', 'from_time', 'to_time', 'available_hours', 'teacher','day')
        read_only_fields = ['available_hours',]

    def create(self, validated_data):
        print(validated_data['from_time'])
        start_time = validated_data['to_time']
        stop_time = validated_data['from_time']

        date = datetime.datetime(1,1,1)
        datetime1 = datetime.datetime.combine(date, start_time)
        datetime2 = datetime.datetime.combine(date, stop_time)
        validated_data['available_hours'] = str(datetime1 - datetime2)

        available = AvailableTime.objects.create(**validated_data)

        return available


class TeacherSerializer(serializers.ModelSerializer):
    isfavorite = serializers.BooleanField(default=False, read_only=True)
    # availableTime = AvailableTimeSerializer(many=True , read_only=True)
    subcategories = SubcategorySerializer(source='subcategory')

    class Meta:
        model = Teacher
        fields = ['id', 'username', 'email', 'subcategory', 'name', 'image', 'phoneNumber','subcategories', 'role', 'teaching_description', 'resume', 'isfavorite','country', 'teacher_type']
        read_only_fields = ['role', 'subcategories']


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ('id', 'review', 'student', 'teacher', 'rate')
        #read_only_fields = ['student']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'comment', 'student')


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lessons
        fields = ('id', 'title', 'price', 'teacher', 'lesson_period')





class PackageLessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageLessons
        fields = ('id', 'title', 'price', 'teacher', 'lesson_period', 'number_of_lessons')


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = ('id', 'reply', 'student', 'post')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model =Favorite
        fields = ('id',  'student', 'teacher')



