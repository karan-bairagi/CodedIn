from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=40)
    profile=models.ImageField(upload_to='profiles/')
    tagline=models.CharField(max_length=200)
    about_me=models.TextField()
    Mobile=models.CharField(max_length=10)
    linkdin_link=models.URLField(null=True,blank=True)
    github_link=models.URLField(null=True,blank=True)
    public_profile=models.BooleanField(default=True)
    view_count=models.IntegerField(default=0)
    security_question=models.CharField(max_length=120,blank=True)
    security_answer=models.CharField(max_length=70,blank=True)
    class Meta:
        db_table='UserProfile'
class ProjectCard(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=60)
    thumbnail=models.ImageField(upload_to='projects/')
    tech_stack=models.CharField(max_length=300)
    project_link=models.URLField()
    live_link=models.URLField(null=True,blank=True)
    class Meta:
        db_table='ProjectCard'
class ProfileVisitor(models.Model):
    profile_owver=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_visitor=models.CharField(max_length=50,blank=True)
    profile_visitor_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='visitor'


class SupportTicket(models.Model):
    full_name=models.CharField(max_length=30)
    user_email=models.EmailField(max_length=60)
    message=models.TextField()
    mobile=models.CharField(max_length=12)
    status=models.CharField(default='pending',max_length=50)
    class Meta:
        db_table='support_ticket'