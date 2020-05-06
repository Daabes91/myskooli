from sqlite3.dbapi2 import Time
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime
import time
from ..system import model
from rest_framework.authtoken.models import Token as DefaultTokenModel
from .utils import import_callable


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
        (3, 'admin'),

    )

    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)


class Student(User):

    name = models.CharField(max_length=60, default=None)
    image = models.CharField(max_length=600, default=None)
    phoneNumber = models.CharField(max_length=14, default=None)

    class Meta:
        verbose_name_plural = "Students"

    def save(self, *args, **kwargs):
        self.role = 1

        super(Student, self).save(*args, **kwargs)


class Teacher(User):
    type_exp = ((1, 'professional'),
        (2, 'community'),)

    name = models.CharField(max_length=60, default=None)
    image = models.CharField(max_length=600, default=None)
    phoneNumber = models.CharField(max_length=14, default=None)
    resume = models.CharField(max_length=600, default=None, null=True)
    subcategory = models.ForeignKey(model.SubCategory, default=None, on_delete=models.CASCADE)
    video = models.CharField(max_length=400, default=None, null=True)
    teacher_type = models.PositiveSmallIntegerField(choices=type_exp , null=True)
    about = models.CharField(max_length=600, default=None, null=True)
    skypeId = models.CharField(max_length=60, default=None, null=True)
    me_as_teacher = models.CharField(max_length=600, default=None, null=True)
    teaching_description = models.CharField(max_length=600, default=None, null=True)
    experience = models.CharField(max_length=600, default=None, null=True)
    certificate = models.CharField(max_length=600, default=None, null=True)
    education = models.CharField(max_length=600, default=None, null=True)
    country = models.ForeignKey(model.Country, default=None, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Teachers"

    def save(self, *args, **kwargs):
        self.role = 2

        super(Teacher, self).save(*args, **kwargs)


TokenModel = import_callable(
    getattr(settings, 'REST_AUTH_TOKEN_MODEL', DefaultTokenModel))


class Post(models.Model):
    comment = models.CharField(max_length=60, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Reviews(models.Model):
    review = models.CharField(max_length=60, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rate = models.IntegerField(default=None)

    def __str__(self):
        return self.review


class Reply(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reply = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.reply


class Favorite(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Lessons(models.Model):
    title = models.CharField(max_length=200, null=False)
    price = models.FloatField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson_period = models.TimeField(default='00:45')

    def __str__(self):
        return self.title


class PackageLessons(models.Model):
    title = models.CharField(max_length=200, null=False)
    price = models.FloatField(default=0)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson_period = models.TimeField(default='00:45')
    number_of_lessons = models.IntegerField(default=0,null=True)

    def __str__(self):
        return self.title


class AvailableTime(models.Model):
    choice = ((1, 'Monday'),
              (2, 'Tuesday'),
              (3, 'Wednesday'),
              (4, 'Thursday'),
              (5, 'Friday'),
              (6, 'Saturday'),
              (7, 'Sunday'),
              )
    day = models.PositiveSmallIntegerField(choices=choice, null=True)
    from_time = models.TimeField(default=None, null=True)
    to_time = models.TimeField(default=None, null=True)
    available_hours = models.TimeField(default=None, null = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='availableTime')










