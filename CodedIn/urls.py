"""
URL configuration for CodedIn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import personal_profile,personal_update,Profile_Visibility,search,forgetten_reset_password,about_developer,add_security
from django.conf.urls.static import static
from app.views import public_profile,delete_user,delete_user_confirm,account_settings,change_password,check_security,token_generate,user_request
from django.conf import settings
from app.views import Dashboard,signup,logout,user_login,user_profile,profile_remove,profile_view,forgettern_password,reset_password,projectcard,project_view,project_delete
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signup,name='signup'),
    path('dash/',Dashboard,name='dashboard'),
    path('',user_login,name='user_login'),
    path('logout',logout,name='logout'),
    path('profile',user_profile,name='profile'),
    path('profile_remove/',profile_remove,name='remove'),
    path('profile_view/',profile_view,name='profile_view'),
    path('forgetten_password/',forgettern_password,name='forgetten_password'),
    path('reset-password/<str:user_token>/',forgetten_reset_password,name='reset_password'),
    path('projectcard/',projectcard,name='projectcard'),
    path('project_view/<int:project_id>/',project_view,name='project_view'),
    path('delete_project/<int:project_id>/',project_delete,name='project_delete'),
    path('public/<str:username>/',public_profile,name='public'),
    path('delete_user/',delete_user,name='delete_user'),
    path('delete/',delete_user_confirm,name='delete_confirm'),
    path('accoount/',account_settings,name='account'),
    path('personal_profile/',personal_profile,name='personal'),
    path('update/',personal_update,name='edit'),
    path('check_password/',change_password,name='checking'),
    path('reset_password/',reset_password,name='reset'),
    path('visibility/',Profile_Visibility,name='public_visibility'),
    path('search/',search,name='search'),
    path('about_developer',about_developer,name='developer_story'),
    path('secure/',add_security,name='security'),
    path('checking/',check_security,name='check'),
    path('token/',token_generate,name='token'),
    path('request/',user_request,name='request_user'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
handler404='app.views.error'
handler500='app.views.error500'
