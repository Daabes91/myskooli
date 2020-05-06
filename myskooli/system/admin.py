from django.contrib import admin
from .model import Category, SubCategory
from . import model

# Register your models here.




admin.site.site_header = "MY SKOOLI SYSTEM ADMIN"
admin.site.site_title = "MY SKOOLI SYSTEM ADMIN"
admin.site.index_title = "Welcome to MY SKOOLI SYSTEM "
admin.site.empty_value_display = '(None)'


@admin.register(model.Category)
class Settings(admin.ModelAdmin):
    list_display = ('category_name', 'category_img')
