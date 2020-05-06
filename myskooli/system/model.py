from django.db import models




# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=60, null=False)
    category_img = models.CharField(max_length=600, default=None)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=60, null=False)
    subcategory_img = models.CharField(max_length=600, default=None)

    def __str__(self):
        return self.subcategory_name


class Country(models.Model):
    country_name = models.CharField(max_length=60, null=False)
    country_img = models.CharField(max_length=600, default=None)

    def __str__(self):
        return self.country_name




