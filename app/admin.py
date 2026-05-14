from django.contrib import admin
from app.models import User,UserProfile,ProjectCard
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ProjectCard)