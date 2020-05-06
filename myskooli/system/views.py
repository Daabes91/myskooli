from django.shortcuts import render
from rest_framework import viewsets, status, request
from .serializers import CategorySerializer, SubcategorySerializer, CountrySerializer
from .model import Category, SubCategory, Country
from ..users.permissions import IsLoggedInUserOrAdmin, IsAdminUser, Anyone


# Create your views here.


class CategoryViews(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'list' :
            permission_classes = [Anyone]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class SubCategoryViews(viewsets.ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = SubCategory.objects.all()
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'list' :
            permission_classes = [Anyone]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class CountryViews(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'list' :
            permission_classes = [Anyone]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]