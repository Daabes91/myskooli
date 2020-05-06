# Create your views here.
from datetime import datetime

from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_jwt.settings import api_settings
from .models import Student, User, Teacher, Reviews, Post, Reply, Favorite, Lessons, PackageLessons, AvailableTime
from .serializers import StudentSignUpSerializer, LoginSerializer, StudentSerializer, \
    TeacherSignUpSerializer, TeacherSerializer, ReviewsSerializer, PostSerializer, ReplySerializer, \
    FavoriteSerializer, LessonsSerializer, PackageLessonsSerializer, AvailableTimeSerializer
from ..users.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsCustomer, IsTeacher

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class StudentSignUpView(viewsets.GenericViewSet):
    serializer_class = StudentSignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = StudentSignUpSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class TeacherSignUp(viewsets.GenericViewSet):
    serializer_class = TeacherSignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = TeacherSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(viewsets.ViewSet):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting

    permission_classes = (permissions.AllowAny,)

    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        username = request.data['username']

        filter_data = User.objects.filter(username=username).values('is_active')
        if filter_data.exists():
            val = filter_data[0]['is_active']
        else:
            return Response("username is not Registered", status=status.HTTP_400_BAD_REQUEST)

        if val:
            if serializer.is_valid():

                user = authenticate(
                    username=request.data['username'], password=request.data['password'])

                if user is not None and user.is_active:  # change according to yourself
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    if user.role == 1:
                        user_role = 'STUDENT'
                    if user.role == 2:
                        user_role = 'TEACHER'
                    if user.role == 3:
                        user_role = 'ADMIN'

                    payload = jwt_payload_handler(user)
                    payload['role'] = user_role
                    payload['id'] = user.pk
                    token = jwt_encode_handler(payload)

                    return Response({'msg': 'Login successful','id':user.pk, 'role': user_role, 'token': token,

                                     'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'Account not approved or wrong Password.'}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'msg': 'Invalid data'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'Error': 'Not a valid user'}, status=status.HTTP_401_UNAUTHORIZED)


class StudenView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_permissions(self):                                                                                                                                                       
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class TeacherView(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data

        fav = Favorite.objects.all()

        for tea in response.data:

            for f in fav:
                if f.teacher.id == tea['id'] and f.student.id == request.user.id:
                    tea['isfavorite'] = True
                    break
                else:
                    tea['isfavorite'] = False

        return response

    def get_permissions(self):
        permission_classes = []
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list':
            permission_classes = [IsLoggedInUserOrAdmin, AllowAny]
        elif  self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ["teacher"]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsCustomer]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id == serializer['student'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response("student that trying to add is not same", status=status.HTTP_401_UNAUTHORIZED)


class CommunityView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id == serializer['student'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response("student that trying to add is not same", status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsCustomer]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsCustomer]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class ReplyView(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsCustomer]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsCustomer]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class FavoriteView(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['student', "teacher"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id == serializer['student'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'msg':"student that trying to add is not same", 'status':status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.id == instance.student.id:
            print(instance.student.id)
            self.perform_destroy(instance)
            return Response({'msg': 'deleted successfully'})
        else:
            return Response({'msg': 'you are not allowed to remove this'})


    def get_permissions(self):

        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsCustomer]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsCustomer]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'destroy':
            permission_classes = [IsCustomer]

        return [permission() for permission in permission_classes]


class LessonsView(viewsets.ModelViewSet):
    serializer_class = LessonsSerializer
    queryset = Lessons.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = [ "teacher"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id == serializer['teacher'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'msg': "teacher that trying to add is not same", 'status': status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        permission_classes = []
        if  self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacher]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsTeacher]
        elif self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class AvailableTimeView(viewsets.ModelViewSet):
    serializer_class = AvailableTimeSerializer
    queryset = AvailableTime.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = [ "teacher"]
    ordering_fields = ['day']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer['to_time'].value)


        if request.user.id == serializer['teacher'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()


            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'msg': "teacher that trying to add is not same", 'status': status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        permission_classes = []
        if  self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacher]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsTeacher]
        elif self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class PackageLessonsView(viewsets.ModelViewSet):
    serializer_class = PackageLessonsSerializer
    queryset =  PackageLessons.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = [ "teacher"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.id == serializer['teacher'].value:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'msg': "teacher that trying to add is not same", 'status': status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        permission_classes = []
        if  self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacher]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsTeacher]
        elif self.action == 'retrieve' or self.action == 'list':
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
