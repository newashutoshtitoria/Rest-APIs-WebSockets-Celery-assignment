from django.contrib import admin
from .models import *

# Register your models here.

# admin.site.register(Image)
@admin.register(Image)
class AppAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


