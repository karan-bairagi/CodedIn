from django import forms
import re
from django.forms import ValidationError
from django.contrib.auth.models import User
from app.models import UserProfile,ProjectCard,SupportTicket
def username_error(value):
    if ' ' in value:
        raise ValidationError('Username cannot contain spaces.')
    if not value[0].isalnum() or not value[-1].isalnum():
        raise ValidationError('Username must start and end with a letter or number.')
    if '..' in value:
        raise ValidationError('Consecutive periods (..) are not allowed.')
    if value.count('.')>=2:
        raise ValidationError('Username can only contain one period (.)')
    if len(value)<=4 or len(value)>20:
        raise ValidationError('Usernames must be between 5 and 20 characters.')
    if len(set(value))==1:
        raise ValidationError('This username is too simple or repetitive.')
    if not re.fullmatch(r'^[a-zA-Z0-9_.]+$',value):
        raise ValidationError('Usernames can only contain letters, numbers, underscores, and periods.')
    if User.objects.filter(username=value).exists():
        raise ValidationError('Username Already Exists')
def password_error(value):
    if len(value)<8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.islower() for char in value):
        raise ValidationError("Password must contain at least one lowercase letter (a-z)")
    if not any(char.isupper() for char in value):
        raise ValidationError('Password must contain at least one uppercase letter (A-Z)')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least one numeric digit (0-9)')
    special_character='!@#$%^&*_.'
    if not any(char in special_character for char in value):
        raise ValidationError('Password must contain at least one special character (e.g., @, #, $, %, &).')
    common_passwords = (
    'pass@123', 'password@123', 'pass#123', 'pass_123',
    'admin@123', 'admin_123', 'admin#123',
    'qwerty@123', 'qwerty_123',
    'welcome@123', 'welcome_123', 'welcome@1')
    if value.lower() in common_passwords:
        raise ValidationError('This password is too common and easy to guess. Choose a stronger one.')
    
    
def email_error(value):
    if User.objects.filter(email__iexact=value.lower()).exists():
        raise ValidationError('This email address is already registered. Please login or use a different email')
    email_list=('@gmail.com','@outlook.com','@yahoo.com')
    if not value.lower().endswith(email_list):
        raise ValidationError('Please enter a valid email address from a trusted provider (e.g., Gmail, Outlook, Yahoo).')

def mobile_error(value):
    value=value.strip()
    if not re.fullmatch(r'^[6-9][0-9]{9}$',value):
        raise ValidationError('Please enter a valid 10-digit mobile number starting with 6, 7, 8, or 9.')
    if len(set(value)) == 1:
        raise ValidationError('Mobile number cannot contain all identical digits.')


def full_name_error(value):
    value=value.strip()
    if len(value) < 3:
        raise ValidationError('Name must be at least 3 characters long.')
    if not re.fullmatch(r'^[A-Za-z ]+$',value):
        raise ValidationError('Name can only contain letters and a single space between words.')
class SignUpForm(forms.ModelForm):
    full_name=forms.CharField(validators=[full_name_error],widget=forms.TextInput(attrs={'placeholder':"Enter your full name"}))
    Mobile=forms.CharField(validators=[mobile_error],widget=forms.TextInput(attrs={'placeholder':'Enter 10-digit mobile number'}))
    email=forms.CharField(validators=[email_error],widget=forms.TextInput(attrs={'placeholder':'username@email.com'}))
    username=forms.CharField(validators=[username_error],widget=forms.TextInput(attrs={'placeholder':'Username','autofocus': True}))
    password=forms.CharField(validators=[password_error],widget=forms.PasswordInput(attrs={'placeholder':'Create a strong password (min. 8 chars)','name':'password'}))
    class Meta:
        model=User
        fields=['username','password','email']

class UserProfileForm(forms.ModelForm):
    tagline=forms.CharField(label='Tagline:',required=False,widget=forms.TextInput(attrs={'placeholder':'e.g., Full Stack Developer | Python Enthusiast','autofocus': True}))
    about_me=forms.CharField(label='About me:',required=False,widget=forms.Textarea(attrs={'placeholder':'Share your professional journey, technical expertise, and core skills...'}))
    profile=forms.ImageField(widget=forms.FileInput,required=False)
    linkdin_link=forms.URLField(label='LinkedIn link:',required=False,widget=forms.URLInput(attrs={'placeholder':'linkedin.com'}))
    github_link=forms.URLField(label='Github link:',required=False,widget=forms.URLInput(attrs={'placeholder':'github.com'}))
    class Meta:
        model=UserProfile
        fields=['profile','about_me','tagline','linkdin_link','github_link']

class ProjectCardForm(forms.ModelForm):
    thumbnail=forms.ImageField(required=False,label='')
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name of your product or repository','autofocus': True}))
    tech_stack=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Comma-separated keywords (e.g., Python, Docker, Next.js)'}))
    project_link=forms.URLField(widget=forms.URLInput(attrs={'placeholder':'Paste your GitHub repository link'}))
    live_link=forms.URLField(required=False,widget=forms.URLInput(attrs={'placeholder':'your-app-url.com'}))
    class Meta:
        model=ProjectCard
        fields=['title','thumbnail','tech_stack','project_link','live_link']
class LoginForm(forms.Form):
    username=forms.CharField(label='Username',widget=forms.TextInput(attrs={'placeholder':'Enter your username','autofocus': True}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'Enter your secure password','name':'password'}))

class Forgetten_Password_Form(forms.Form):
    New_Password=forms.CharField(validators=[password_error],widget=forms.PasswordInput(attrs={'placeholder':'Enter a strong new password','autofocus': True,'name':'password'}))
    confirm=forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'placeholder':'Re-type your new password to confirm','name':'password'}))
class Forgetten_email(forms.Form):
    new_email=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your registered email address','autofocus': True}))

def personal_username_error(value):
    if ' ' in value:
        raise ValidationError('Username cannot contain spaces.')
    if not value[0].isalnum() or not value[-1].isalnum():
        raise ValidationError('Username must start and end with a letter or number.')
    if '..' in value:
        raise ValidationError('Consecutive periods (..) are not allowed.')
    if value.count('.')>=2:
        raise ValidationError('Username can only contain one period (.)')
    if len(value)<=4 or len(value)>20:
        raise ValidationError('Usernames must be between 5 and 20 characters.')
    if len(set(value))==1:
        raise ValidationError('This username is too simple or repetitive.')
    if not re.fullmatch(r'^[a-zA-Z0-9_.]+$',value):
        raise ValidationError('Usernames can only contain letters, numbers, underscores, and periods.')
def personal_email_error(value):
    email_list=('@gmail.com','@outlook.com','@yahoo.com')
    if not value.lower().endswith(email_list):
        raise ValidationError('Please enter a valid email address from a trusted provider (e.g., Gmail, Outlook, Yahoo).')
class Personal_Form(forms.ModelForm):
    full_name=forms.CharField(validators=[full_name_error],widget=forms.TextInput(attrs={'placeholder':'Update your full name','autofocus': True}))
    username=forms.CharField(validators=[personal_username_error],widget=forms.TextInput(attrs={'placeholder':'Change your unique username'}))
    email=forms.CharField(validators=[personal_email_error],widget=forms.TextInput(attrs={'placeholder':'update-email@example.com'}))
    mobile=forms.CharField(validators=[mobile_error],widget=forms.TextInput(attrs={'placeholder':'Update your 10-digit mobile number'}))
    class Meta:
        model=User
        fields=['full_name','username','email','mobile']
class check_password_Form(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your current password to verify','autofocus': True,'name':'password'}))

class Public_Profile_Form(forms.Form):
    profile_select={
        True:'Public',
        False:'Private'
    }
    pvt_pbl=forms.ChoiceField(choices=profile_select,widget=forms.RadioSelect,initial=True,label="Profile Visibility")
    

class Security_Questions_Form(forms.Form):
    SECURITY_OPTIONS = [
        ('', '--- Please select a security question ---'),
        ('What was the name of the first company you worked at?','What was the name of the first company you worked at?'),
        ("What is your mother's maiden name?","What is your mother's maiden name?"),
        ("In what hospital or clinic were you born?", 'In what hospital or clinic were you born?'),
        ("What was the name of your primary/elementary school?", 'What was the name of your primary/elementary school?'),
        ("What was the mascot of your high school?", 'What was the mascot of your high school?'),
    ]
    questions=forms.ChoiceField(choices=SECURITY_OPTIONS,required=True,widget=forms.Select())
    answer=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Provide your confidential answer here...','autofocus':True}))


class Request_User_Form(forms.ModelForm):
    full_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your registered full name..','class': 'form-input'}))
    user_email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter your registered account email..','class': 'form-input'}))
    mobile=forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'Enter your registered 10-digit mobile number...','class': 'form-input','maxlength': '10'}))
    message=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Describe your issue briefly (e.g., "I have lost access to both my password and security answers. Please verify my parameters and reset my account credentials.")...', 'class': 'form-input','rows': '4'}))
    class Meta:
        model = SupportTicket
        fields = ['full_name', 'user_email', 'mobile', 'message']