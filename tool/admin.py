from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Tool,PreDefineTools

admin.site.register(Tool)
admin.site.register(PreDefineTools)
