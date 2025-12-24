from django.contrib import admin
from .models import Category, Video, Pdf

# Register your models here.
admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Pdf)
