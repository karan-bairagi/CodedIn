from django.contrib import admin
from app.models import User,UserProfile,ProjectCard
from chat.models import ChatRoom,Message
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ProjectCard)
admin.site.register(ChatRoom)
admin.site.register(Message)