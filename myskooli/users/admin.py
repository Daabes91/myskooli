from django.contrib import admin

from .models import Student, Teacher
from . import models

# Register your models here.




admin.site.site_header = "MY SKOOLI SYSTEM ADMIN"
admin.site.site_title = "MY SKOOLI SYSTEM ADMIN"
admin.site.index_title = "Welcome to MY SKOOLI SYSTEM "
admin.site.empty_value_display = '(None)'


@admin.register(models.Student)
class Settings(admin.ModelAdmin):
    list_display = ('name', 'phoneNumber')


@admin.register(models.Teacher)
class Settings(admin.ModelAdmin):
    list_display = ('name', 'phoneNumber')


# Register your models here.
