from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = "Zad Al-Seghar Admin"
admin.site.site_title = "Zad Al-Seghar Admin Portal"

admin.site.register(Prophet)
admin.site.register(Video)
admin.site.register(PDF)