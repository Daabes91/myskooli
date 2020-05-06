from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj == request.user)
        print(request.user)
        username = str(request.user)
        s = str(obj)

        return s == username or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class Anyone(permissions.BasePermission):
    def has_permission(self, request, view):

        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsCustomer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if str(request.user) == 'AnonymousUser':
            return False
        else:

            return request.user and request.user.role == 1

    def has_permission(self, request, view):
        if str(request.user) == 'AnonymousUser':
            return False
        else:
            print(request.user)

            return request.user and request.user.role == 1


class IsTeacher(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if str(request.user) == 'AnonymousUser':
            return False
        else:

            return request.user and request.user.role == 2

    def has_permission(self, request, view):
        if str(request.user) == 'AnonymousUser':
            return False
        else:

            return request.user and request.user.role == 2
